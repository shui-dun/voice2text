# voice2text

## 安装方法

- clone该项目
- 在百度大脑申请[语音识别api](https://ai.baidu.com/tech/speech)
- 创建 `baiduKey.py` 文件，添加百度大脑的 `apiKey` 和 `secretKey` 两个变量
- `pip install -r requirements.txt`

## 功能

- 可以拖动窗口
- 点击 `start` ，便开始录制音频
	![image-20220119223217546](assets/image-20220119223217546.png)
- 点击 `stop` ，结束录制，识别到的文字会复制到剪切板
	![image-20220119223313969](assets/image-20220119223313969.png)
- 按`q`，关闭窗口