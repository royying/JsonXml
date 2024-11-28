import json
import tkinter as tk
import ctypes
import xmltodict
import requests
import xml.dom.minidom as minidom

# Set DPI awareness for high DPI monitors
ctypes.windll.shcore.SetProcessDpiAwareness(2)


def convert_text_manual(type):
    convert_text(textarea_response.get("1.0", "end-1c"), type)


def convert_text(text, type):
    if "xml" == type:
        flat_node = xml_convert(text)  # Pass the text to the converter function
    elif "json" == type:
        node_dict = json_convert(json.loads(text))
        flat_node = ""
        for k, v in node_dict.items():
            flat_node += f"\"{k}\", is(notNullValue()),\n"

    textarea_b.delete("1.0", "end")  # Clear the current contents of textarea B
    textarea_b.insert("1.0", flat_node)  # Insert the converted text into textarea B


def clear_text():
    textarea_response.delete("1.0", "end")


def clear_get():
    textarea_url.delete("1.0", "end")  # Clear the current contents of textarea B


def requestBy(method):
    url = textarea_url.get("1.0", "end-1c")  # Get the text from textarea
    body = textarea_body.get("1.0", "end-1c")
    textarea_response.delete("1.0", "end")

    try:
        if method == "get":
            response = requests.get(url, verify=False)
        elif method == "post":
            if len(body) > 0:
                response = requests.post(url, verify=False, json=json.loads(body))
            else:
                response = requests.post(url, verify=False)
        print(response.status_code)
    except Exception as error:
        print(str(error))
        textarea_response.insert("1.0", "Can't reach\n\n")

    content_type = response.headers.get("Content-Type") or ""
    if "xml" in content_type:
        pretty_response = beautify_xml(response.text)
        convert_text(pretty_response, "xml")
    elif "json" in content_type:
        pretty_response = beautify_json(response.text)
        convert_text(response.text, "json")
    else:
        pretty_response = response.text

    print("\nResponse:\n")
    print(pretty_response)

    textarea_response.insert("1.0", pretty_response)  # Insert the converted text into textarea A


def beautify_xml(xml_string):
    dom = minidom.parseString(xml_string)
    pretty_xml = dom.toprettyxml(indent="  ")
    return pretty_xml


def beautify_json(json_string):
    parsed_json = json.loads(json_string)
    pretty_json = json.dumps(parsed_json, indent=2, sort_keys=True)
    return pretty_json


def flatten_xml(d, parent_key='', sep='.'):
    """
    Flatten a nested dictionary by joining keys with a separator.
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_xml(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, item in enumerate(v):
                new_item_key = f"{new_key}[{i}]"
                if isinstance(item, dict):
                    items.extend(flatten_xml(item, new_item_key, sep=sep).items())
                else:
                    items.append((f"{new_item_key}", item))
        else:
            items.append((new_key, v))
    return dict(items)


def xml_convert(str):
    xml_dict = xmltodict.parse(str)

    # Flatten the dictionary using '_' as the separator
    flat_dict = flatten_xml(xml_dict)
    result = ""
    for k, v in flat_dict.items():
        result = result + "\n" + f"\"{k.replace('.#text', '')}\", isA(String.class),"
    result = result.strip()[:-1]
    return result


def json_convert(json_obj, prefix=''):
    flattened = {}
    try:
        for key, value in json_obj.items():
            new_key = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                flattened.update(json_convert(value, new_key))
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    if isinstance(item, dict):
                        flattened.update(json_convert(item, f"{new_key}[{i}]"))
                    else:
                        flattened[f"{new_key}[{i}]"] = item
            else:
                flattened[new_key] = value
    except:
        print(json_obj)
    return flattened


def paste_from_clipboard():
    textarea_url.delete("1.0", "end")
    clipboard_content = root.clipboard_get()
    textarea_url.insert("insert", clipboard_content)


def format_switch():
    content = textarea_url.get("1.0", "end")
    if "json" in content:
        content = content.replace("json", "xml")
    elif "xml" in content:
        content = content.replace("xml", "json")
    textarea_url.delete("1.0", "end")
    textarea_url.insert("1.0", content.strip())


# Create the main window
# root = ThemedTk(theme="arc")
root = tk.Tk()

root.title("JSON XML converter")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the desired window size
window_width = int(screen_width * 0.7)
window_height = int(screen_height * 0.8)

# Set the window size
root.geometry(f"{window_width}x{window_height}")

root.tk_setPalette(background='#444', foreground='white', activeBackground='#444', activeForeground='white',
                   selectColor='#111')

button_frame = tk.Frame(root)
# Create the widgets

frame_url = tk.Frame(root)
frame_body = tk.Frame(root)
frame_url_btn = tk.Frame(root)

label_url = tk.Label(frame_url, text="Url")
textarea_url = tk.Text(frame_url, font="consolas", height=1)

label_body = tk.Label(frame_body, text="Body")
textarea_body = tk.Text(frame_body, font="consolas", height=1)

get_btn = tk.Button(frame_url_btn, text="Get", command=lambda: requestBy("get"), bg="green")
post_btn = tk.Button(frame_url_btn, text="post", command=lambda: requestBy("post"), bg="blue")
paste_btn = tk.Button(frame_url_btn, text="Paste", command=paste_from_clipboard)
format_switch_btn = tk.Button(frame_url_btn, text="JSON<-->XML", command=format_switch)
clear_get_btn = tk.Button(frame_url_btn, text="Clear", command=clear_get, bg="red")

label_a = tk.Label(root, text="Input")
textarea_response = tk.Text(root, font="consolas")

label_b = tk.Label(root, text="Output")
textarea_b = tk.Text(root, font="consolas")

convert_json_btn = tk.Button(button_frame, text="Convert JSON", command=lambda: convert_text_manual("json"))
convert_xml_btn = tk.Button(button_frame, text="Convert XML", command=lambda: convert_text_manual("xml"))
clear_btn = tk.Button(button_frame, text="Clear", command=clear_text)
button_copy = tk.Button(root, text="Copy", command=lambda: root.clipboard_append(textarea_b.get("1.0", "end")))

# Add the widgets to the window
frame_url.pack(side="top", fill="x")
frame_body.pack(side="top", fill="x")
frame_url_btn.pack(side="top", fill="x", pady=10)

label_url.pack(side=tk.LEFT)
textarea_url.pack(padx=10, pady=10, expand=True, fill='x', side=tk.RIGHT)

label_body.pack(side=tk.LEFT)
textarea_body.pack(padx=10, pady=10, expand=True, fill='x', side=tk.RIGHT)

get_btn.pack(side="left", padx=5)
post_btn.pack(side="left", padx=5)
paste_btn.pack(side="left", padx=5)
format_switch_btn.pack(side="left", padx=5)
clear_get_btn.pack(side="right", padx=5)

label_a.pack()
textarea_response.pack(expand=False, fill='x', padx=20)

convert_json_btn.pack()
convert_xml_btn.pack()
clear_btn.pack()

button_frame.pack(side="top", fill="x", pady=10)
convert_json_btn.pack(side="left", padx=5)
convert_xml_btn.pack(side="left", padx=5)
clear_btn.pack(side="right", padx=5)

label_b.pack()
textarea_b.pack(expand=True, fill='both', padx=20, pady=10)
button_copy.pack(side="left", padx=5, pady=10)
# Start the main event loop
root.mainloop()
