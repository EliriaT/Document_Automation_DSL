from fpdf import FPDF

size = 16
font = "times"

class PDF(FPDF):
    def init(self):
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font(font, '', size)

    def align(self, alignment, text):
        alignText = self.checkingAlignment(alignment)
        if alignText != -1:
            self.cell(0, 10, text, align=alignText, ln=1)

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
        if textStyle.lower() == "bold":
            styleTo = 'B'
        elif textStyle.lower() == "underline":
            styleTo = 'U'
        elif textStyle.lower() == "italics":
            styleTo = 'I'
        elif textStyle.lower() == '':
            styleTo = ''
        else:
            print("NO SUCH TEXT STYLE.")
            return -1
        return styleTo

    def text(self, textStyle, text):
        styleTo = self.checkingStyle(textStyle)
        if styleTo != -1:
            self.set_font(font, styleTo, size)
            self.cell(0, 10, text, ln=1)
    
    def textAlign(self, textStyle, text, alignment):
        styleTo = self.checkingStyle(textStyle)
        alignTo = self.checkingAlignment(alignment)
        if styleTo != -1 and alignTo != -1:
            self.set_font(font, styleTo, size)
            self.cell(0, 10, text, align=alignTo, ln=1)

    def textFontSize(self, textStyle, text, fontTo, sizeTo):
        styleTo = self.checkingStyle(textStyle)
        if styleTo != -1:
            self.set_font(fontTo, styleTo, sizeTo)
            self.cell(0, 10, text, ln=1)

    def checkingColor(self, color):
        if color.lower() == "red":
            pdf.set_text_color(255,0,0)
        elif color.lower() == "green":
            pdf.set_text_color(0,255,0)
        elif color.lower() == "blue":
            pdf.set_text_color(0,0,255)
        elif color.lower() == "black":
            pdf.set_text_color(0,0,0)
        elif color.lower() == "magenta":
            pdf.set_text_color(255,0,255)
        elif color.lower() == "yellow":
            pdf.set_text_color(255,255,0)
        elif color.lower() == "brown":
            pdf.set_text_color(150,75,0)
        elif color.lower() == "gray":
            pdf.set_text_color(128,128,128)
        else: 
            print("NO SUCH COLOR AS", color.lower())
            return -1
        return 1

    def textColor(self, textColor, text):
        if self.checkingColor(textColor) == 1:
            self.cell(0, 10, text, ln=1)

    def color(self, color):
        self.checkingColor(color)

    def fontSize(self, fontTo, sizeTo):
        self.set_font(fontTo, '', sizeTo)
        font = fontTo
        size = sizeTo

    def font(self, fontTo):
        self.set_font(fontTo, '', size)
        font = fontTo

    def size(self, sizeTo):
        self.set_font(font, '', sizeTo)
        size = sizeTo

    def print(self, title):
        title = title+".pdf"
        self.output(title)

pdf = PDF('P', 'mm', 'Letter')
pdf.init()
pdf.textAlign("bold", "Title", "center")
pdf.text("italics", "italic check")
pdf.text("bold", "bold check")
pdf.text("underline", "underline check")
pdf.textColor("blue", "blue text check")
pdf.fontSize('helvetica', 20)
pdf.textColor("yellow", "yellow 20 text check")
pdf.color("black")
pdf.textFontSize('', "times in 40", "times", 40)
pdf.text("", "simple text")
pdf.print("Test")