import os
import json
import matplotlib.pyplot as plt
import numpy as np

def process_json_files(database_folder):
    age_data = []
    pointing_error_data = []
    perspective_error_data = []

    for filename in os.listdir(database_folder):
        if filename.endswith('.json'):
            with open(os.path.join(database_folder, filename)) as f:
                data = json.load(f)
                age = int(data["MetaData"]["Player_Age"])
                
                # Extract the pointing and perspective error data
                pointing_errors = []
                perspective_errors = []

                for task in data["Sessions"]["Egocentric"][0]["PointingTasks"]:
                    for judgement in task["PointingJudgements"]:
                        pointing_errors.append(judgement["Absolute_Error"])
                
                for trial in data["Sessions"]["PerspectiveTaking"][0]["Trials"]:
                    perspective_errors.append(trial["ErrorMeasure"])

                # Use mean error per session for plotting
                age_data.append(age)
                pointing_error_data.append(np.mean(pointing_errors))
                perspective_error_data.append(np.mean(perspective_errors))

    return age_data, pointing_error_data, perspective_error_data

def create_age_norms_plot(database_folder, new_file):
    # Process all JSON files in the database folder
    age_data, pointing_error_data, perspective_error_data = process_json_files(database_folder)

    # Process the new JSON file
    with open(new_file) as f:
        new_data = json.load(f)
        new_age = int(new_data["MetaData"]["Player_Age"])

        new_pointing_errors = []
        new_perspective_errors = []

        for task in new_data["Sessions"]["Egocentric"][0]["PointingTasks"]:
            for judgement in task["PointingJudgements"]:
                new_pointing_errors.append(judgement["Absolute_Error"])

        for trial in new_data["Sessions"]["PerspectiveTaking"][0]["Trials"]:
            new_perspective_errors.append(trial["ErrorMeasure"])

        new_pointing_error = np.mean(new_pointing_errors)
        new_perspective_error = np.mean(new_perspective_errors)

    # Create the plot
    plt.figure(figsize=(12, 5))

    # Subplot for Pointing Error
    plt.subplot(121)
    plt.scatter(age_data, pointing_error_data, label='Existing Data')
    plt.scatter(new_age, new_pointing_error, color='red', label='New Data', marker='*', s=150)
    plt.title('Egocentric_PointingError')
    plt.xlabel('Age group')
    plt.ylabel('Raw score')
    plt.legend()

    # Subplot for Perspective Taking Error
    plt.subplot(122)
    plt.scatter(age_data, perspective_error_data, label='Existing Data')
    plt.scatter(new_age, new_perspective_error, color='red', label='New Data', marker='*', s=150)
    plt.title('PerspectiveTaking_Error')
    plt.xlabel('Age group')
    plt.ylabel('Raw score')
    plt.legend()

    # Save the plot
    plt.tight_layout()
    plt.savefig('age_norms_with_new_data_plot.png')
    plt.close()