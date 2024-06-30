# Multi-Agent LLM Approach

This repository focuses on a Multi-Agent LLM approach in which different agents are able to answer qualitative and quantitative questions.

![alt text](/images/demo_ui.png)


## Usage

Make sure you have Python version 3.10 or above installed. 
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements.
I recommend using a virtual environment before installing the requirements.

```bash
pip install -r requirements.txt
```

It is needed to install ollama and download the relevant model (llama3) locally. Please refer to the [ollama documentation](https://ollama.com/) for that.

Before running the pipeline or the chat tool, you have to run the Redis docker container (add -d if you want to run it in the backround).
```bash
docker compose up -d
```

In order to process the datasets please run the pipeline as the following.
```bash
python pipeline.py
```
In case you want to run the embedding creation, please ensure to set the relevant variable to true inside of the pipeline.py file.

## Tool
In case you want to run the chat tool, make sure that all the relevant datasets are available by running the pipeline first. 
Once the pipeline is finished, you can start the demo as the following.
```bash
streamlit run app.py
```

## Author
[@pascal-wolf](https://github.com/pascal-wolf)
