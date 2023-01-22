import imgkit

table = '''
<!DOCTYPE html>
<html>
<body>

<p>我会显示 €</p>
<p>我会显示 €</p>
<p>我会显示 €</p>

</body>
</html>

'''
imgkit.from_string(table, 'out1.jpg')