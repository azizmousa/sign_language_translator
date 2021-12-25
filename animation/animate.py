
import cv2


class SignOut:
    def __init__(self,path):
        self.caps   = []
        self.vid = 0
        self.flag = True
        self.speed = 20
        self.path = path

    def preprocess(self , phrase):
        return phrase.split(' ')

    def display(self):
        while self.flag:
            frame = None
            ret , frame = self.caps[self.vid].read()
            if ret == False:
                if self.vid != len(self.caps) - 1:
                    ret , frame = self.caps[self.vid+1].read()
                else:
                    self.flag = False
                    [cap.release() for cap in self.caps]
                    cv2.destroyAllWindows()
                    break
                self.vid += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow('frame' , gray)
            if cv2.waitKey(self.speed) & 0xFF == ord('q'):
                break

    def show_sign(self , phrase):
        words  = self.preprocess(phrase)
        videos = [self.path+'/'+word+'.mp4' for word in words]
        self.caps   = [cv2.VideoCapture(video) for video in videos]
        self.display()

    def setSpeed(self , speed):
        self.speed = speed

# so = SignOut('videos')
# so.setSpeed(5)
# so.show_sign('I love egypt')