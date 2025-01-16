#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include <sys/wait.h>
#include <sys/ioctl.h>

#include "gio/gio.h"
#include "glib.h"

char *audio_file_path = NULL;
GtkWidget *output_label = NULL;
GtkWidget *output_image = NULL;
FILE *auralize_backend = NULL;
GThread *backend_thread = NULL;

GtkWidget *pick_audio_button = NULL;
GtkWidget *classify_button = NULL;

int pipe_front2back[2];

gpointer handle_backend(gpointer data) {
    pid_t pid = 0;
    int pipe_back2py [2];
    int pipe_py2back [2];
    char py_buf[256];
    char front_buf[256];
    char msg[256];
    int status;

    pipe(pipe_back2py);
    pipe(pipe_py2back);
    pid = fork();
    if (pid == 0) {
        // python process
        dup2(pipe_back2py[0], STDIN_FILENO);
        dup2(pipe_py2back[1], STDOUT_FILENO);
        close(pipe_back2py[1]);
        close(pipe_py2back[0]);
        if (execl("./auralize.py", "./auralize.py", (char*)NULL) < 0) {
            puts("execl error");
            exit(1);
        }
    }
    // back process
    close(pipe_back2py[0]);
    close(pipe_py2back[1]);

    read(pipe_py2back[0], py_buf, 256);
    if (strcmp(py_buf, "ready\n") != 0) {
        printf("backend error in python: %s\n", py_buf);
        return NULL;
    }
    // unblock buttons
    puts("unblocking buttons");
    gtk_widget_set_sensitive(pick_audio_button, true);

    while (read(pipe_front2back[0], front_buf, 256) > 0) {
        if (strcmp(front_buf, "e\n") == 0) break;

        if (strcmp(front_buf, "a\n") == 0) { // new audio
            gtk_widget_set_sensitive(pick_audio_button, false);
            gtk_widget_set_sensitive(classify_button, false);
            read(pipe_front2back[0], front_buf, 256);
            gtk_label_set_text(GTK_LABEL(output_label), "Generating spectrogram...");
            write(pipe_back2py[1], "audio\n", 7);
            memset(msg, 0, strlen(msg));
            strcpy(msg, audio_file_path);
            strcat(msg, "\n");
            write(pipe_back2py[1], msg, strlen(msg));
            read(pipe_py2back[0], py_buf, 256);
            gtk_label_set_text(GTK_LABEL(output_label), audio_file_path);
            gtk_image_set_from_file(GTK_IMAGE(output_image), "spectrogram.png");
            gtk_widget_set_sensitive(classify_button, true);
            gtk_widget_set_sensitive(pick_audio_button, true);
            continue;
        }

        if (strcmp(front_buf, "c\n") == 0) {
            continue;
        }

        printf("FRONT_BUF CONTENTS:\n%s\nFRONT_BUF CONTENTS END;\n", front_buf);
        memset(front_buf, 0, strlen(front_buf));
    }

    puts("killing python");
    write(pipe_back2py[1], "exit\n", 5);
    wait(NULL);
    puts("python killed");
    close(pipe_front2back[0]);
    close(pipe_front2back[1]);
    return NULL;
}

void on_file_picked(GObject *gobject, GAsyncResult *result, gpointer data) {
    GFile *file = gtk_file_dialog_open_finish(GTK_FILE_DIALOG(data), result, NULL);
    if (file == NULL) return;
    audio_file_path = g_file_get_path(file);
    write(pipe_front2back[1], "a\n", 3);
    write(pipe_front2back[1], audio_file_path, 256);
}

void open_audio_picker() {
    GtkFileDialog *file_dialog;
    GtkFileFilter *filter;

    filter = gtk_file_filter_new();
    gtk_file_filter_add_suffix(filter, "wav");

    file_dialog = gtk_file_dialog_new();
    gtk_file_dialog_set_default_filter(file_dialog, filter);
    gtk_file_dialog_open(file_dialog, NULL, NULL, on_file_picked, file_dialog);
}

void classify_audio() {
    write(pipe_front2back[1], "c\n", 3);
}

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window;

    GtkWidget *menu_box;
    GtkWidget *h_box;
    GtkWidget *buttons_box;
    GtkWidget *output_box;

    GtkWidget *button;
    GtkWidget *logo;

    window = gtk_application_window_new (app);
    gtk_window_set_title (GTK_WINDOW(window), "Auralize");
    gtk_window_set_default_size (GTK_WINDOW(window), 200, 200);

    menu_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_window_set_child(GTK_WINDOW(window), menu_box);
    gtk_widget_set_halign(menu_box, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(menu_box, GTK_ALIGN_CENTER);

    logo = gtk_image_new();
    gtk_image_set_from_file(GTK_IMAGE(logo), "logo.png");
    gtk_image_set_pixel_size(GTK_IMAGE(logo), 200);
    gtk_box_append(GTK_BOX(menu_box), logo);

    GtkWidget *separator;
    separator = gtk_separator_new(GTK_ORIENTATION_VERTICAL);
    gtk_box_append(GTK_BOX(menu_box), separator);

    h_box = gtk_box_new(GTK_ORIENTATION_HORIZONTAL, 10);
    gtk_box_append(GTK_BOX(menu_box), h_box);
    gtk_widget_set_halign(h_box, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(h_box, GTK_ALIGN_CENTER);

    buttons_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_box_append(GTK_BOX(h_box), buttons_box);
    gtk_widget_set_halign(buttons_box, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(buttons_box, GTK_ALIGN_CENTER);

    output_box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_box_append(GTK_BOX(h_box), output_box);
    gtk_widget_set_halign(output_box, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(output_box, GTK_ALIGN_CENTER);

    pick_audio_button = gtk_button_new_with_label ("Pick audio");
    g_signal_connect(pick_audio_button, "clicked", G_CALLBACK(open_audio_picker), NULL);
    gtk_box_append(GTK_BOX(buttons_box), pick_audio_button);
    gtk_widget_set_sensitive(pick_audio_button, false);

    classify_button = gtk_button_new_with_label("Classify");
    g_signal_connect(classify_button, "clicked", G_CALLBACK(classify_audio), NULL);
    gtk_box_append(GTK_BOX(buttons_box), classify_button);
    gtk_widget_set_sensitive(classify_button, false);

    button = gtk_button_new_with_label ("Quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_window_destroy), window);
    gtk_box_append(GTK_BOX(buttons_box), button);

    output_label = gtk_label_new("No audio picked");
    gtk_box_append(GTK_BOX(output_box), output_label);

    output_image = gtk_image_new_from_file("spectrogram_example.png");
    gtk_image_set_pixel_size(GTK_IMAGE(output_image), 200);
    gtk_box_append(GTK_BOX(output_box), output_image);

    gtk_window_present(GTK_WINDOW(window));
    gtk_window_maximize(GTK_WINDOW(window));
}

gpointer start_backend() {
    pipe(pipe_front2back);
    gpointer backend_thread = g_thread_new("auralize.backend", handle_backend, NULL);
    return backend_thread;
}

int main(int argc, char** argv) {
    GtkApplication *app;
    int status;

    app = gtk_application_new("si.auralize", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    backend_thread = start_backend();
    status = g_application_run(G_APPLICATION (app), argc, argv);
    write(pipe_front2back[1], "e\n", 3);
    g_thread_join(backend_thread);
    g_object_unref(app);

    return status;
}
