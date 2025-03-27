from textnode import TextNode, TextType

def main():
    sample = TextNode("This is some anchor text", TextType.BOLD, "https://www.boot.dev")
    print(repr(sample))

main()
