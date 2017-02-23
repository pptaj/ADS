opyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/minimal-notebook

MAINTAINER Jupyter Project <jupyter@googlegroups.com>

USER root

# libav-tools for matplotlib anim
RUN apt-get update && \
    apt-get clean && \
        rm -rf /var/lib/apt/lists/*

	USER $NB_USER

	# Install Python 3 packages
	# Remove pyqt and qt pulled in for matplotlib since we're only ever going to
	# use notebook-friendly backends in these images
	RUN conda install --quiet --yes \
	    'nomkl' \
	        'ipywidgets=5.2*' \
		    'pandas=0.19*' \
		        'numexpr=2.6*' \
			    'matplotlib=1.5*' \
			        'scipy=0.17*' \
				    'beautifulsoup4=4.5.*' \
				        'xlrd'  && \
					    conda remove --quiet --yes --force qt pyqt && \
					        conda clean -tipsy

						#ADD  https://github.com/pptaj/ADS C:/adsrepo/ADS/Part1Latest.ipynb

						ADD Untitled.py Untitled.py
						CMD ["python","Untitled.py"]

