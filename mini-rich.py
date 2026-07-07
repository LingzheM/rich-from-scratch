SGR = {
    "bold": "1", "dim": "2", "italic": "3", "underline": "4",
    "black": "30", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "magenta": "35", "cyan": "36", "white": "37",
}

class Style:
    def __init__(self, bold=False, underline=False, color=None, bgcolor=None):
        self.bold = bold
        self.underline = underline
        self.color = color
        self.bgcolor = bgcolor

    
    def _codes(self):
        # 建一个 list，把该开的参数塞进去，用；拼接起来。
        codes = []
        if self.bold:
            codes.append(SGR["bold"])
        if self.underline:
            codes.append(SGR["underline"])
        if self.color:
            codes.append(SGR[self.color])
        if self.bgcolor:
            codes.append()
        return ";".join(codes)
    

    def render(self, text):
        codes = self._codes()
        if not codes:
            return text
        return f"\x1b[{codes}m{text}\x1b[0m"


    def __repr__(self):
        # dunder: 决定在终端里打印这个对象时长什么样
        return f"Style(bold={self.bold}, underline={self.underline}, color={self.color!r})"
    

    @classmethod
    def parse(cls, spec):
        bold = False
        color = None
        bgcolor = None
        next_is_bg = None
        for word in spec.split():
            if word == "bold":
                bold = True
            elif word == "on":
                next_is_bg = True
            elif word in SGR:
                if next_is_bg:
                    bgcolor = word
                    next_is_bg = False
                else:
                    color = word
        return cls(bold=bold, color=color, bgcolor=bgcolor)

def cprint(text, style=""):
    print(Style.parse(style).render(text))


def main():
    cprint("Error!", "bold red")
    cprint("OK", "green")
    cprint("普通文字")


if __name__ == "__main__":
    main()