from fpdf import FPDF


class PDF(FPDF):
    def init(self):
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.size=16
        self.font="times"
        self.set_font(self.font, '', self.size)


    def align(self, alignment, text):
        alignText = self.checkingAlignment(alignment)
        if alignText != -1:
            self.multi_cell(0, 10, text, align=alignText)

    def checkingAlignment(self, alignment):
        if alignment.lower() == "center":
            alignText = 'C'
        elif alignment.lower() == "left":
            alignText = 'L'
        elif alignment.lower() == "right":
            alignText = 'R'
        else:
            print("NO SUCH ALIGNMENT.")
            return -1
        return alignText

    def checkingStyle(self, textStyle):
        if textStyle.lower() == "b":
            styleTo = 'B'
        elif textStyle.lower() == "u":
            styleTo = 'U'
        elif textStyle.lower() == "i":
            styleTo = 'I'
        elif textStyle.lower() in ["ibu","biu","iub","bui","uib","ubi"]:
            styleTo = 'IBU'
        elif textStyle.lower() in ["iu","ui"]:
            styleTo = 'IU'
        elif textStyle.lower() in ["ib","bi"]:
            styleTo = 'IB'
        elif textStyle.lower() in ["bu","ub"]:
            styleTo = 'BU'
        elif textStyle.lower() == '':
            styleTo = ''
        else:
            print("NO SUCH TEXT STYLE.")
            return -1
        return styleTo

    def text(self, textStyle, text):
        styleTo = self.checkingStyle(textStyle)
        if styleTo != -1:
            self.set_font(self.font, styleTo, self.size)
            self.write(h=self.size-8,txt=text)
        # self.set_font(self.font, '', self.size)
    
    def textAlign(self, textStyle, text, alignment):
        styleTo = self.checkingStyle(textStyle)
        alignTo = self.checkingAlignment(alignment)
        if styleTo != -1 and alignTo != -1:
            self.set_font(self.font, styleTo, self.size)
            self.multi_cell(0, h=self.size-8, txt=text, align=alignTo)

    def textFontSize(self, textStyle, text, fontTo, sizeTo):
        styleTo = self.checkingStyle(textStyle)
        if styleTo != -1:
            self.set_font(fontTo, styleTo, sizeTo)
            self.write(h=self.size-8,txt=text)

    def checkingColor(self, color):
        if color.lower() == "red":
            self.set_text_color(255,0,0)
        elif color.lower() == "green":
            self.set_text_color(0,255,0)
        elif color.lower() == "blue":
            self.set_text_color(0,0,255)
        elif color.lower() == "black":
            self.set_text_color(0,0,0)
        elif color.lower() == "magenta":
            self.set_text_color(255,0,255)
        elif color.lower() == "yellow":
            self.set_text_color(255,255,0)
        elif color.lower() == "brown":
            self.set_text_color(150,75,0)
        elif color.lower() == "gray":
            self.set_text_color(128,128,128)
        else: 
            print("NO SUCH COLOR AS", color.lower())
            return -1
        return 1

    def textColor(self, textColor, text):
        if self.checkingColor(textColor) == 1:
            self.write(h=self.size-8,txt=text)
        self.color("black")

    def color(self, color):
        self.checkingColor(color)

    def fontSize(self, fontTo, sizeTo):
        self.set_font(fontTo, '', sizeTo)
        self.font = fontTo
        self.size = sizeTo

    def print(self, title):
        title = title+".pdf"
        self.output(title)

pdf = PDF('P', 'mm', 'Letter')
pdf.init()
pdf.textAlign("b", "Title", "right")
pdf.text("I", "italic checkkkk   lalalalalala   ")
pdf.text("I", "\n ")
pdf.text("I", "\n ")
pdf.text("I", "italic checkkkk   lalalalalala")
pdf.print("Test")