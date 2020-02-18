# Инсталиране на Tensorflow -- Linux
След проби и грешки споделям този лесен начин за инсталиране на Tensorflow с Nvidia GPU, Ubuntu 18.04 и Anaconda 5.3, от нула:

1. С нова инсталация на Ubuntu 18.04, добавяте драйвера на Nvidia, както е описано в (1).  по този начин ubuntu-drivers се грижи за забраняване на open source драйвера, който идва по default.  в момента работи ОК с версия 415.  намира всички налични Nvidia GPU.
2. Инсталирате CUDA Toolkit 10.0 от nvidia.com -- 1.7GB download за конкретната OS.  в моя случай Linux / x86_64 / Ubuntu / 18.04 / deb(local)
3. Инсталирате Anaconda 5.3 от anaconda.com
4. Следвате описанието на този агент (2) за добавяне на Tensorflow GPU:  conda create --name tf_gpu tensorflow-gpu   В (2) има малко typo, след инсталацията conda Ви дава правилната команда за активиране на новия environment: conda activate tf_gpu   До тук всичко работи в терминал, а tf_gpu environment се грижи да превключва между Python 3.6.6, които работи с ТФ и последния 3.7+ и съответните версии на другите tensorflow dependencies.
5. За да работи tf и в Jupyter Notebook, добавете nb_conda (3) extension manager, който добавя меню за превключване на environments в browser-a: conda install nb_conda
готово.

 
## Източници
1. https://linuxconfig.org/how-to-install-the-nvidia-drivers-on-ubuntu-18-04-bionic-beaver-linux
2. https://towardsdatascience.com/tensorflow-gpu-installation-made-easy-use-conda-instead-of-pip-52e5249374bc
3. https://anaconda.org/anaconda/nb_conda или https://docs.anaconda.com/anaconda/user-guide/tasks/use-jupyter-notebook-extensions/
