# RAMP starting-kit - Relative Humidity Prediction in Morocco

Authors : Zakaria Akil, Zakarya Elmimouni, Ahmed Khairaldin, Amine Razig, Khadija slim, Yassine Oj

 ---
 
<p align="center">
  <!-- Logo du haut (centré) -->
  <img src="Img/ippLogo.png" alt="Logo Haut" width="25%">
  <br><br>
  <!-- Logos du bas (gauche et droite) -->
  <img src="Img/S5-45_C3S_logo.png" alt="Logo Gauche" width="20%" style="margin-right: 20px;">
  &nbsp;&nbsp;&nbsp;&nbsp;
  <img src="Img/Copernicus vecto def  Europe's eyes on Earth.png" alt="Logo Droite" width="20%" style="margin-left: 20px;">
</p>

## Getting started

### Install

To run a submission and the notebook you need to install the dependencies listed
in `requirements.txt`. You can do this with the
following command-line:

```bash
pip install -U -r requirements.txt
```

If you are using `conda`, we provide an `environment.yml` file for similar
usage.

### Challenge description

> **Context** :  
> Relative Humidity is a measure of how much moisture is in the air compared to the maximum amount it can hold at a given temperature. It is expressed as a percentage, where 100% means the air is fully saturated with water vapor and cannot hold any more, leading to possible condensation (such as dew or fog).  
>  
> The ability of air to hold moisture depends on temperature—warmer air can contain more water vapor, while cooler air holds less. This is why humidity often feels higher in warm weather, even if the actual amount of water vapor in the air hasn’t changed. For example, if the relative humidity is 50%, it means the air contains half the moisture it could potentially hold at that temperature. A high relative humidity (like 80–90%) makes the air feel damp and heavy, while a low relative humidity (like 20–30%) makes it feel dry, which can cause discomfort such as dry skin or irritation.  
>  
> In the Moroccan geographical area, relative humidity plays a vital role in predicting droughts, managing water resources, and understanding climate variability. The country’s semi-arid and arid regions are highly sensitive to fluctuations in humidity, which affect soil moisture and crop yields. Low relative humidity accelerates evaporation from reservoirs and irrigation systems, intensifying water scarcity. In coastal and mountainous areas, humidity variations influence cloud formation and precipitation patterns, impacting agriculture and hydropower generation. By integrating relative humidity data into climate models, scientists and policymakers can better anticipate drought risks and optimize water management strategies to mitigate their effects.



Get started with the [relative_humidity_prediction_starting_kit](relative_humidity_prediction_starting_kit.ipynb)


### Test a submission

The submissions need to be located in the `submissions` folder. For instance
for `my_submission`, it should be located in `submissions/my_submission`.

To run a specific submission, you can use the `ramp-test` command line:

```bash
ramp-test --submission my_submission
```


You can get more information regarding this command line:

```bash
ramp-test --help
```

### To go further

You can find more information regarding `ramp-workflow` in the
[dedicated documentation](https://paris-saclay-cds.github.io/ramp-docs/ramp-workflow/stable/using_kits.html)


