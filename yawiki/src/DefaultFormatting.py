'''
Created on 03.05.2010

@author: alarin
'''
from WikiSettingsModels import PageFormattingSetting
formatting = []
formatting.append(PageFormattingSetting(pattern=r"'''text'''", regex_pattern=r"'''([\w/<>]+)'''", target=r"<i>\1</i>"))
formatting.append(PageFormattingSetting(pattern=r"''text''", regex_pattern=r"''([\w/<>]+)''", target=r"<strong>\1</strong>"))
formatting.append(PageFormattingSetting(pattern=r"''text''", regex_pattern=r"\[BR\]", target=r"<br />"))