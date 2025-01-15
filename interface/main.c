#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "gio/gio.h"
#include "glib.h"

char *audio_file_path = NULL;
GtkWidget *output_label = NULL;
GtkWidget *output_image = NULL;
FILE *auralize_backend = NULL;
GThread *backend_thread = NULL;

int pipe_front2back[2];

gpointer handle_backend(gpointer data) {
    pid_t pid = 0;
    int pipe_back2py [2];
    int pipe_py2back [2];
    char buf[256];
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
        execl("python", "auralize.py");
        exit(1);
    }
    // back process

    return NULL;
}

void on_file_picked(GObject *gobject, GAsyncResult *result, gpointer data) {
    GFile *file = gtk_file_dialog_open_finish(GTK_FILE_DIALOG(data), result, NULL);
    if (file == NULL) return;
    audio_file_path = g_file_get_path(file);
    printf("Opened %s\n", audio_file_path);
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

gpointer generate_spectrogram(gpointer data) {
    if (audio_file_path == NULL) {
        gtk_label_set_text(GTK_LABEL(output_label), "Choose a file first");
        return false;
    }
    gtk_label_set_text(GTK_LABEL(output_label), "Generating spectrogram...");
    const char* COMMAND_BASE = "python auralize.py ";
    char* command = malloc(strlen(COMMAND_BASE) + strlen(audio_file_path) + 1);
    if (command == NULL) return false;
    strcpy(command, COMMAND_BASE);
    strcat(command, audio_file_path);
    puts(command);
    int exit_code = system(command);
    if (exit_code) {
        gtk_label_set_text(GTK_LABEL(output_label), "Error generating spectrogram");
        return false;
    }
    gtk_image_set_from_file(GTK_IMAGE(output_image), "spectrogram.png");
    gtk_label_set_text(GTK_LABEL(output_label), "Spectrogram generated");
    free(command);
    puts("finished spectrogram");
    return false;
}

void classify_audio() {
    backend_thread = g_thread_new("auralize.spectrogram_thread", generate_spectrogram, NULL);
}

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window;

    GtkWidget *menu_box;
    GtkWidget *h_box;
    GtkWidget *buttons_box;
    GtkWidget *output_box;

    GtkWidget *button;
    GtkWidget *logo;

    if (pipe(pipe_front2back) < 0) {
        puts("pipe error");
        return;
    }

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

    button = gtk_button_new_with_label ("Pick audio");
    g_signal_connect(button, "clicked", G_CALLBACK(open_audio_picker), NULL);
    gtk_box_append(GTK_BOX(buttons_box), button);

    button = gtk_button_new_with_label("Classify");
    g_signal_connect(button, "clicked", G_CALLBACK(classify_audio), NULL);
    gtk_box_append(GTK_BOX(buttons_box), button);

    button = gtk_button_new_with_label ("Quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_window_destroy), window);
    gtk_box_append(GTK_BOX(buttons_box), button);

    output_label = gtk_label_new("Select a file to analyze");
    gtk_box_append(GTK_BOX(output_box), output_label);

    output_image = gtk_image_new_from_file("spectrogram_example.png");
    gtk_image_set_pixel_size(GTK_IMAGE(output_image), 200);
    gtk_box_append(GTK_BOX(output_box), output_image);

    gtk_window_present(GTK_WINDOW(window));
    gtk_window_maximize(GTK_WINDOW(window));
}

int main(int argc, char** argv) {
    GtkApplication *app;
    int status;

    app = gtk_application_new("si.auralize", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    status = g_application_run(G_APPLICATION (app), argc, argv);
    puts("goodbye");
    g_object_unref(app);

    return status;
}
