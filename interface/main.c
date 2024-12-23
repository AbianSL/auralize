#include "gio/gio.h"
#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* audio_file_path = NULL;

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
    gtk_file_filter_add_suffix(filter, "mp3");

    file_dialog = gtk_file_dialog_new();
    gtk_file_dialog_set_default_filter(file_dialog, filter);
    gtk_file_dialog_open(file_dialog, NULL, NULL, on_file_picked, file_dialog);
}

void classify_audio() {
    if (audio_file_path == NULL) return;
    const char* COMMAND_BASE = "python auralize.py ";
    char* command = malloc(strlen(COMMAND_BASE) + strlen(audio_file_path) + 1);
    if (command == NULL) return;

    strcpy(command, COMMAND_BASE);
    strcat(command, audio_file_path);
    puts(command);
    // system(command); // wait until we have the python program for classification
    free(command);
}

static void activate(GtkApplication* app, gpointer user_data) {
    GtkWidget *window;
    GtkWidget *box;
    GtkWidget *button;
    GtkWidget *logo;

    window = gtk_application_window_new (app);
    gtk_window_set_title (GTK_WINDOW(window), "Auralize");
    gtk_window_set_default_size (GTK_WINDOW(window), 200, 200);

    box = gtk_box_new(GTK_ORIENTATION_VERTICAL, 10);
    gtk_window_set_child(GTK_WINDOW(window), box);
    gtk_widget_set_halign(box, GTK_ALIGN_CENTER);
    gtk_widget_set_valign(box, GTK_ALIGN_CENTER);

    logo = gtk_image_new();
    gtk_image_set_from_file(GTK_IMAGE(logo), "logo.png");
    gtk_image_set_pixel_size(GTK_IMAGE(logo), 200);
    gtk_box_append(GTK_BOX(box), logo);

    button = gtk_button_new_with_label ("Pick audio");
    g_signal_connect(button, "clicked", G_CALLBACK(open_audio_picker), NULL);
    gtk_box_append(GTK_BOX(box), button);

    button = gtk_button_new_with_label("Classify");
    g_signal_connect(button, "clicked", G_CALLBACK(classify_audio), NULL);
    gtk_box_append(GTK_BOX(box), button);

    button = gtk_button_new_with_label ("Quit");
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(gtk_window_destroy), window);
    gtk_box_append(GTK_BOX(box), button);

    gtk_window_present(GTK_WINDOW(window));
    gtk_window_maximize(GTK_WINDOW(window));
}

int main(int argc, char** argv) {
    GtkApplication *app;
    int status;

    app = gtk_application_new("si.auralize", G_APPLICATION_DEFAULT_FLAGS);
    g_signal_connect(app, "activate", G_CALLBACK(activate), NULL);
    status = g_application_run(G_APPLICATION (app), argc, argv);
    g_object_unref (app);

    return status;
}
