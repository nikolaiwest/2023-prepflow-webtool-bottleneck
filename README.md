# PrEPFlow-Webtool

PrEPFlow-Webtool is a web application powered by Dash, a Python web framework for creating interactive, web-based data visualizations and applications.

## Table of contents
* [Overview](#overview)
* [Installation](#installation)
* [Webtool](#webtool)
    * [Data selection](#data-selection)
    * [Bottleneck Detection](#bottleneck-detection)
    * [Bottleneck Diagnosis](#bottleneck-diagnosis)
    * [Bottleneck Prediction](#bottleneck-prediction)
* [Acknowledgements](#acknowledgements)
* [License](#license)
* [Contributions](#Contributions)

## Overview

This Dash app provides a user-friendly interface to interact with and visualize data related to PrEPFlow. It includes features to set up and customize the app's language settings, display dynamic content, and handle user interactions. The app's functionality is organized into components and callbacks for a modular and maintainable code structure.

## Installation

https://prepflow.pythonanywhere.com/selection 

Before running the app, make sure to install the required dependencies. You can use pip to install them:

    ```pip install -r requirements.txt```


To run the PrEPFlow-Webtool app, use the following command:

    python app.py

The app will start a local development server, and you can access it by opening a web browser and navigating to http://localhost:8050 or the URL provided in the console.

## Configuration

You can configure the app's behavior by modifying the settings in the CONFIG_APP and CONFIG_DATA dictionaries found in the code.
Internationalization

The app supports multiple languages. You can customize the user's language by changing the CONFIG_APP["user_language"] setting and providing translation files in the "locale" directory.

## Project Structure

    app.py: The main script to run the Dash app.
    src/components: Contains modules for defining the app's layout and components.
    src/auxiliaries/callbacks: Includes callback functions for handling user interactions.
    src/auxiliaries/storage: Stores configuration data.



## Acknowledgements

The webtool [**BottleNext**](https://prepflow.pythonanywhere.com/selection) was developed by the [RIF Institute for Research and Transfer e.V.](https://www.rif-ev.de/) as part of the research project [PrEPFlow](https://ips.mb.tu-dortmund.de/forschen-beraten/prepflow/) (Grant number: 21595) of the [Bundesvereinigung Logistik e.V. (BVL)](https://www.bvl.de/). It was developed through the close cooperation with the [Institute for Production Systems](https://ips.mb.tu-dortmund.de/) at the [Technical University of Dortmund](https://www.tu-dortmund.de/). 

It is is being funded by the [German Federation of Industrial Research Associations "Otto von Guericke" e.V. (AiF)](https://www.aif.de/) as part of the [Program to promote Joint Industrial Research and Development (IGF)](https://www.aif.de/foerderangebote/igf-industrielle-gemeinschaftsforschung.html).

## License

This project is licensed under the [your license here] License - see the LICENSE file for details.

Please replace [your license here] with the appropriate license information for your project, such as "MIT," "Apache 2.0," or any other license you choose. Additionally, create a LICENSE file in your project directory with the full license text or a link to the license text online.

## Contributions
We welcome contributions to this repository. If you have a feature request, bug report, or proposal, please open an issue. If you wish to contribute code, please open a pull request.