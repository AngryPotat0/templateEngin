# python_source = """\
# SEVENTEEN = 17

# def three():
#     return 3
# """
# global_namespace = {}
# exec(python_source, global_namespace)
# print(global_namespace['SEVENTEEN'])
# print(global_namespace['three']())
# t = "12"
# print("""result.append(%s)""" % repr(t))

code = """
def render_function(context):
    c_viewsDict = context['viewsDict']
    result = []
    result.extend(['<p>',str(c_viewsDict),'</p>\n<p>',str(abs(c_viewsDict['name'])),'</p>\n'])
    return "".join(result)
"""

functions = {}
exec(code,functions)
print(functions)