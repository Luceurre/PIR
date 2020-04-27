library(readr);

data<-read_csv("~/PycharmProjects/PIR/data/data_4.csv");

get_devices_id <- function(data) {
  get_devices_id <- unique(data$device);
}

get_nb_location_by_id <- function(data) {
  devices_id <- get_devices_id(data);
  count <- c();
  
  for(id in devices_id) {
    data_device <- subset(data, data$device == id);
    count <- c(count, length(unique(data_device$ID_sejour_1km)));
  }
  
  get_nb_location_by_id <- as.data.frame(cbind(devices_id, count));
}

get_study_duration_by_id <- function(data) {
  devices_id <- get_devices_id(data);
  count <- c();
  for(id in devices_id) {
    data_device <- subset(data, data$device == id);
    count <- c(count, length(unique(data_device$jour)));
  }
  
  get_study_duration_by_id <- as.data.frame(cbind(devices_id, count));
}

get_mean_nb_location_by_id <- function(data) {
  devices_id <- get_devices_id(data);
  nb_location_by_id <- get_nb_location_by_id(data);
  study_duration <- get_study_duration_by_id(data);
  mean <- c();
  
  for(i in c(1:length(devices_id))) {
    mean <- c(mean, as.numeric(nb_location_by_id[i, 2]) / as.numeric(study_duration[i, 2]))
  }
  
  get_mean_nb_location_by_id <- as.data.frame(cbind(devices_id, mean));
}

get_nb_location_by_id_and_day <- function(data) {
  devices_id <- get_devices_id(data);
  for(id in devices_id) {
    data_id <- subset(data, data$device == id);
    id_days <- unique(data_id$jour);
    for(day in id_days) {
      count <- length(unique(data_id$jour == day));
    }
  }
}

get_variance_nb_location_by_id <- function(data) {
  mean <- get_mean_nb_location_by_id(data);
  variance <- c();
  for(i in c(1:nrow(mean))) {
     id <- mean[i, 1];
     data_id <- subset(data, data$device == id);
     days <- unique(data_id$jour);
     var <- 0;
     mean_id <- as.numeric(mean[i, 2]);
     for(day in days) {
      data_day <- subset(data_id, data_id$jour == day);
      nb_loc <- as.numeric(length(unique(data_day$ID_sejour_1km)));
      var <- var + (mean_id - nb_loc) * (mean_id - nb_loc);
     }
     variance <- c(variance, var / 14);
  }
  
  get_variance_nb_location_by_id <- as.data.frame(cbind(mean, variance));
}

devices_id <- get_devices_id(data);
nb_location_by_id <- get_nb_location_by_id(data);
study_duration <- get_study_duration_by_id(data);
mean_nb_location_by_id <- get_mean_nb_location_by_id(data);
variance_nb_location_by_id <- get_variance_nb_location_by_id(data);
