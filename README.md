# PrEPFlow-Webtool


## Table of contents
* [Overview](#overview)
* [Webtool](#webtool)
* [Installation](#installation)
* [Acknowledgements](#acknowledgements)
* [Contributions](#Contributions)
* [License](#license)

## Overview

The [**BottleNext**](https://prepflow.pythonanywhere.com/selection) webtool provides a user-friendly interface to interact with and visualize data related to manufacturing bottlenecks. It provides additional features to set up and customize the app's language settings and visual display. 

The webapp  is build using [Dash](https://plotly.com/dash/), a powerful Python web framework that helps to create interactive, data-driven web applications. It combines the simplicity of Python with the flexibility of HTML, CSS, and JavaScript, enabling the development of responsive web applications for data visualization, analytics, and user interaction.

## Webtool

The webtool is available online and allows to perform a bottleneck analysis in a web browser. The deployment was done withPythonAnywhere, a cloud-based platform that allows running and deploying Python applications and websites without the need for server maintenance.

* Webtool: https://prepflow.pythonanywhere.com/selection 


The strucuture of the webtool **BottleNext** is based on a holistic approach to industrial bottleneck analysis:

![Phases for bottleneck analysis](https://github.com/nikolaiwest/2023-prepflow-webtool-bottleneck/blob/main/assets/webtool-preview-model.png)

This approach divides the bottleneck analysis into the four phases Detection, Diagnosis, Prognosis and Prescription. At this point, we refrain from a detailed description of the phases and instead refer to the publications issued in the course of the work. 

* **Bottleneck Detection**
    * West, N., Syberg, M., Deuse, J. (2022). A Holistic Methodology for Successive Bottleneck Analysis in Dynamic Value Streams of Manufacturing Companies. In: Andersen, AL., et al. Towards Sustainable Customization: Bridging Smart Products and Manufacturing Systems. CARV MCPC 2021 2021. Lecture Notes in Mechanical Engineering. Springer, Cham. DOI: [10.1007/978-3-030-90700-6_69](https://doi.org/10.1007/978-3-030-90700-6_69)
    * West, N., Schwenken, J., Deuse, J. (2022). Comparative Study of Methods for the Real-Time Detection of Dynamic Bottlenecks in Serial Production Lines. In: Fujita, H., Fournier-Viger, P., Ali, M., Wang, Y. (eds) Advances and Trends in Artificial Intelligence. Theory and Practices in Artificial Intelligence. IEA/AIE 2022. Lecture Notes in Computer Science, vol 13343. Springer, Cham. DOI: [10.1007/978-3-031-08530-7_1](https://doi.org/10.1007/978-3-031-08530-7_1)

* **Bottleneck Diagnosis**
    * West, N.; Schwenken, J.; Deuse, J. (2023): Data-driven approach for diagnostic analysis of dynamic bottlenecks in serial manufacturing systems. In: Electrical Engineering Systems and Systems Science, System Control (arXiv). DOI: [10.48550/arXiv.2306.16120](https://doi.org/10.48550/arXiv.2306.16120)

* **Bottleneck Prediction** 
    * West, N., Deuse, J. (2023):  Multivariate time series forecasting for multi-step prediction of throughput bottlenecks using Long Short-Term Memory networks. In: Proceedings of the International Conference On Recent Challenges In Engineering And Technology (ICRcET). Preprint available: [here](https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet/blob/main/WEST-E%7E1.PDF)

The web tool uses four menu options, which are described in the following sections. 

![Preview of the Webtool's header](https://github.com/nikolaiwest/2023-prepflow-webtool-bottleneck/blob/main/assets/webtool-preview-header.png)

### Data Selection 

To enable a flexible example, the web tool allows data for bottleneck analysis to be provided in three different ways. 

![Preview of the Webtool's selection](https://github.com/nikolaiwest/2023-prepflow-webtool-bottleneck/blob/main/assets/webtool-preview-selection.png)

#### Use sample data
The sample data originates from a value stream with five workstations S and six buffers B. The value stream is directed and the system boundaries are unconstrained. The process time pt was set to `2.00`, with stations S1 and S3 having additional process time of `2.25`. The maximum capacity of buffers bc was set to `5 parts` for all buffers. The data set comprises 10 million time steps and is fully available [online](https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet).

The merit of this data set is that it can be applied quickly. Both the simulation and the use of own data are associated with longer calculation times, whereby the duration depends considerably on the selected parameters. Here, a model has already been pre-trained for the example data set, so the forecast can also be viewed quickly. An in-depth description of this use case can be found in further detail in our [publication on bottleneck forecasting]((https://github.com/nikolaiwest/2023-bottleneck-prediction-icrcet/blob/main/WEST-E%7E1.PDF)), which serves as the basis for this web tool.

#### Simulate new data
With the help of a simulation, a new data set can be generated and used in the bottleneck analysis. Thus, comparable use cases can be tested without the need for existing data. In addition to the simulation, the calculation of the active operating periods also takes place in this step. The process is associated with longer range times. 10,000 time steps at five stations require about 15 minutes of calculation time.

#### Use your own data
In addition, own data from a value stream can be used. Two data sets must be uploaded for this purpose.

1. The **buffer levels** contain the time as index, as well as an attribute per available buffer. This attribute indicates how many parts are currently stored in the buffer. The maximum fill level must not be exceeded. The following is an exemplary excerpt of the data set.
2. The **active operating periods** contain information on the duration that the existing stations are active. There is a separate attribute for each station. In addition, the `bottleneck` attribute contains information about which station is currently active for the longest time. The following is an exemplary excerpt of the data set.

### Bottleneck Detection

The bottleneck detection provides a visual evaluation of the selected bottleneck data. For this purpose, three characteristic plots are generated: 

1. **Bottlenecks during the observation period:** According to the *Theory of Constraints*, every system has at all times exactly one bottleneck. The plot displays the current bottleneck in the data set during every point in time of the observation period. 
2. **Buffer level during the observation period:** The buffer level is limited by the defined buffer capacity. As such, the plot of the buffer levels shows the current number of semi-finished products in each buffer, never exceeding the maximum capacity.
3. **Active periods during the observation period:** According to the *Active Period Method*, the station with the longest active period is the current bottleneck. The plot displays the characteristic saw tooth profile of the current active periods of all stations.

### Bottleneck Diagnosis

As part of the bottleneck diagnosis, the *bottleneck frequency*, *bottleneck severity* and *bottleneck costs* are to be visualized. These metrics were not the main focus of the project work, which is why they have only been implemented in rudimentary form in the web tool to date. 

However, they are part of a planned research project, called *Detection and diagnostics of dynamic bottlenecks in directional Material flow systems through retrofittable buffer level monitoring* (DeDiFlow). It will deal in particular with the detection and diagnosis of dynamic bottlenecks in directed material flow systems under consideration of buffer levels. 

Please [contact us](mailto:nikolai.west@rif-ev.de) if you are interested in participating in the project committee.

### Bottleneck Prediction

Two parameters must be set before performing the bottleneck prediction. The look-back window specifies the length of the time series used for training. The forecast horizon specifies the length of the forecast.

The results of the prediction are displayed using the ratio of correctly predicted bottleneck stations. The results are compared to four benchmarks. 

1. The benchmark `random` predicts bottlenecks randomly. 
2. The benchmark`naiveM2` predicts only station S1 as bottleneck 
3. The benchmark`naiveM4` predicts only station S3 as bottleneck 
4. The benchmark `last` predicts the last station in the training dataset as bottleneck.

Lastly, exemplary visualizations of the predictions can be displayed. The two left plots show the input variables of the prediction. The right plot ("Truth and predictions") shows the comparison of the prediction as LSTM prediction and the actual course of the bottleneck. The selection of the test data was set in advance to observations with a bottleneck change in order to exclude trivial predictions.

## Installation

If you prefer to run the analysis yourself, you can simply follow these steps: 

1. **Clone the Repository:** Clone this repository to your local machine 
2. **Install Dependencies:** Set up a new env using [requirements.txt](https://github.com/nikolaiwest/2023-prepflow-webtool-bottleneck/blob/main/requirements.txt)
3. **Run the Project:** You can now run the project.    
    ``` 
    python app.py
    ```

4. The app will start a local development server, and you can access it by opening a web browser and navigating to `http://localhost:8050` or the URL provided in the console.

## Acknowledgements

The webtool [**BottleNext**](https://prepflow.pythonanywhere.com/selection) was developed by the [RIF Institute for Research and Transfer e.V.](https://www.rif-ev.de/) as part of the research project [PrEPFlow](https://ips.mb.tu-dortmund.de/forschen-beraten/prepflow/) (Grant number: 21595) of the [Bundesvereinigung Logistik e.V. (BVL)](https://www.bvl.de/). It was developed through the close cooperation with the [Institute for Production Systems](https://ips.mb.tu-dortmund.de/) at the [Technical University of Dortmund](https://www.tu-dortmund.de/). 

It is is being funded by the [German Federation of Industrial Research Associations "Otto von Guericke" e.V. (AiF)](https://www.aif.de/) as part of the [Program to promote Joint Industrial Research and Development (IGF)](https://www.aif.de/foerderangebote/igf-industrielle-gemeinschaftsforschung.html).

## License

This project is licensed under the MIT License - see the [license file](https://github.com/nikolaiwest/2023-prepflow-webtool-bottleneck/blob/main/LICENSE) for details.

## Contributions
We welcome contributions to this repository. If you have a feature request, bug report, or proposal, please open an issue. If you wish to contribute code, please open a pull request.