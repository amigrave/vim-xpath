try:
    #vim module is only available when run from inside vim
    import vim
except ImportError:
    vim = None
    
from vim_xml_tools import xpath as x
from vim_xml_tools.exceptions import XPathError

VARIABLE_SCOPE = "s:"

def get_current_buffer_string():
    return "\n".join(vim.current.buffer)

def evaluate_xpath_on_current_buffer(xpath):
    loc_list = VimLocListAdaptor()
    loc_list.clear_current_list()
    
    xml = get_current_buffer_string()

    try:
        results = x.evaluate(xml, xpath, {})
        if len(results) > 0:
            for result in results:
                loc_list.add_result_entry(result)
        else:
            loc_list.add_error_entry('No results returned')
    except XPathError as e:
        loc_list.add_error_entry(e.message)

class VimLocListAdaptor(object):

    def clear_current_list(self):
        vim.eval("setloclist(0, [], 'r')")

    def add_result_entry(self, result):
        bufnr_arg = "'bufnr': {0}, ".format(vim.current.buffer.number)

        lnum_arg = ""
        if result["line_number"] is not None:
            lnum_arg = "'lnum': {0}, ".format(result["line_number"])

        text = result["match"]
        if result["value"] != "":
            text += ": {0}".format(result["value"])

        text_arg = "'text': '{0}', ".format(text)

        vim.eval("setloclist(0, [{" + 
                bufnr_arg + lnum_arg + text_arg + "}], 'a')")

    def add_error_entry(self, error_text):
        vim.eval(("setloclist(0, [{{" +
                  "'bufnr': {0}, " +
                  "'type': 'E', " +
                  "'text': '{1}'" +
                  "}}], 'a')"
                 ).format(vim.current.buffer.number, error_text))
