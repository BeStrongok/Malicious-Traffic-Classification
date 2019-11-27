# Malicious-Traffic-Classification
## 项目简介
- **主要任务**：从数据处理到算法建模再到结果分析，构建一个端到端的恶意流量分类模型
- **数据集**：10种恶意软件所产生的流量，格式为pcap文件
- **算法**：卷积神经网络，2个卷积层以及2个全连接层
## 具体流程
- 环境准备
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
- 数据处理
  - 每个类别对应一个pcap包，存放在0_pcap文件夹中
  - 拆包，将pcap进行session层面的拆分
    ```
    pwsh 1_Pcap2Session.ps1 -s
    如果是按照flow层面进行拆分
    $ pwsh 1_Pcap2Session.ps1 -f
    ```
  
