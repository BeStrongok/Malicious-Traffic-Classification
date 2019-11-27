# Malicious-Traffic-Classification
## **项目简介**
- **主要任务**：从数据处理到算法建模再到结果分析，构建一个端到端的恶意流量分类模型
- **数据集**：10种恶意软件所产生的流量，格式为pcap文件
- **算法**：卷积神经网络，2个卷积层以及2个全连接层
## 具体流程
- **环境准备**
  - Mono  
    ```
    $ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    $ sudo apt install apt-transport-https ca-certificates
    $ echo "deb https://download.mono-project.com/repo/ubuntu stable-xenial main" | sudo tee /etc/apt/sources.list.d/mono-official-stable.list
    $ sudo apt update
    $ sudo apt install mono-devel
    ```
  - PowerShell Core
    ```
    $ wget -q https://packages.microsoft.com/config/ubuntu/16.04/packages-microsoft-prod.deb
    $ sudo dpkg -i powershell_6.1.0-1.ubuntu.16.04_amd64.deb
    $ sudo apt-get install -f
    ```
  - fdupes
    ```
    $ sudo apt-get install fdupes
    ```
- **数据处理**
  - 每个类别对应一个pcap文件，存放在1_pcap文件夹中
  - 拆包，将pcap文件进行session层面的拆分
    ```
    $ pwsh 1_Pcap2Session.ps1 -s
    如果是按照flow层面进行拆分
    $ pwsh 1_Pcap2Session.ps1 -f
    如果成功运行，则可以看到2_Session文件夹中含有AllLayers/和L7/这两个文件夹
    ```
  - 对pcap包进行预处理，主要是进行下采样以及进行padding操作，统一到784个字节
    ```
    $ pwsh 2_ProcessSession.ps1 -a [-u | -s]
    其中-u表示随机进行下采样，而-s表示对pcap包进行按size从大到小后再进行下采样，采样60000个包  
    如何执行成功则在3_ProcessedSession文件夹中包含两个文件夹，FilteredSession/和TrimedSession/分别对应下采样和padding操作后的文件夹
    ```
  - 将pcap包进行转图像操作
    ```
    python3 3_Session2png.py
    得到的结果保存在4_Png/文件夹中，每个样本一个文件夹
    ```  
- **模型训练**
  - 加载数据
    代码保存在load_dataset.py中，作为模块提供给训练脚本进行导入
  - 模型训练
    代码保存在train.ipynb中，使用**tensorflow2.0**进行模型的构建与训练
- **模型结果**
  - 
  
