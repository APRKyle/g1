import jetson




class Output:
    def __init__(self, ip=None, path=None):

        self.ip = ip
        self.videoPath = path

    def initOutput(self):

        if self.ip:
            self.streamOutput = jetson.utils.videoOutput(f'rtp://{self.ip}:15000')

        if self.videoPath:
            self.videoSaver = jetson.utils.videoOutput(f'file://{self.videoPath}')

    def Render(self, image):
        output = jetson.utils.cudaFromNumpy(image)
        if self.ip:
            self.streamOutput.Render(output)
        if self.videoPath:
            self.videoSaver.Render(output)



