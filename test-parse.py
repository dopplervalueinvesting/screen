import urllib
import lxml
import lxml.html 
import re

url_local1 = "http://www.smartmoney.com/quote/FAST/?story=financials&timewindow=1&opt=YB&isFinprint=1&framework.view=smi_emptyView" 
result1 = urllib.urlopen(url_local1)
element_html1 = result1.read()
doc1 = lxml.html.document_fromstring (element_html1)
list_row1 = doc1.xpath(u'.//th[div[contains(text(),"Total Assets")]]/following-sibling::td/text()')
print list_row1

url_local2 = "http://finance.yahoo.com/q/bs?s=FAST" 
result2 = urllib.urlopen(url_local2)
element_html2 = result2.read()

print element_html2
doc2 = lxml.html.document_fromstring (element_html2)
list_row2 = doc2.xpath(u'.//td[strong[contains(text(),"Total Assets")]]/following-sibling::td/strong/text()') 
print list_row2
       
# SMARTMONEY
"""
<tr class="odd bold">
	<th><div style='font-weight:bold'>Total Assets</div></th>
	<td>  1,684,948</td>
	<td>  1,468,283</td>								
	<td>  1,327,358</td>								
	<td>  1,304,149</td>									
	<td>  1,163,061</td>
</tr>
"""

# YAHOO
"""
<tr>
	<td colspan="2"><strong>Total Assets</strong></td>
	<td align="right"><strong>1,684,948&nbsp;&nbsp;</strong></td>
	<td align="right"><strong>1,468,283&nbsp;&nbsp;</strong></td>
	<td align="right"><strong>1,327,358&nbsp;&nbsp;</strong></td>
</tr>
"""

