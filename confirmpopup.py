from kivy.properties import StringProperty
from os.path import join, dirname
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.app import App
import re

Builder.load_file(join(dirname(__file__), 'confirmpopup.kv'))


class ConfirmPopup(Popup):
    title_text = StringProperty('Updates Available')
    sentence_text= StringProperty('Do you whant to update now?')
    update = None
    ok_text = StringProperty('OK')
    cancel_text = StringProperty('Cancel')
    update_text = StringProperty("Informacao")

    __events__ = ('on_ok', 'on_cancel')

    def ok(self):
        self.dispatch('on_ok')
        self.dismiss()

    def cancel(self):
        self.dispatch('on_cancel')
        self.dismiss()


    def on_ok(self):
        global update
        update=True
        App.get_running_app().stop()
        pass

    def on_cancel(self):
        global update
        update = False
        App.get_running_app().stop()
        pass
    def get_update(self):
        global update
        return update
    def set_updateInformation(self,information,version,betaAlphaVersion,beta_or_stable_or_alpha):
        information=re.split('\\\\n ',information)
        if beta_or_stable_or_alpha=="beta":
            improvements="Version: Beta "+version+" - "+betaAlphaVersion+" \n"
        elif beta_or_stable_or_alpha=="alpha":
            improvements="Version: Alpha "+version+" - "+betaAlphaVersion+" \n"
        else:
            improvements="Version: "+version+" \n"
        for phrase in information:
            improvements = improvements + phrase + " \n"
        self.update_text= (improvements)

class PopupTest(App):
    update = None
    content = None
    def build(self):
        global content
        content.open()


    def get_update(self):
        global content
        return content.get_update()

    def set_updateInformation(self,information,version,betaAlphaVersion,beta_or_stable_or_alpha):
        global content
        content=ConfirmPopup()
        content.set_updateInformation(information,version,betaAlphaVersion,beta_or_stable_or_alpha)
