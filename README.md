# Weathergov Django Frontend Experiment
## Running
We are using the [current weathergov repo](https://github.com/weathergov/weather.gov) as a submodule here, so that we can keep the site assets up to date easily for the time being. Therefore when cloning this repo, you need to run:
```
git clone --recurse-submodules <url-you-use-for-this-repo>
```
  
After you have cloned the repository, you can run `make zap` to set up the containers. Visit [http://localhost:8080]() to see the application live once the containers are running
