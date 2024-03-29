from crypto.aes import AESdecryptCBC
import struct

"""
    iOS 4 keychain-2.db data column format

    version     0x00000000
    key class   0x00000008
                kSecAttrAccessibleWhenUnlocked                      6
                kSecAttrAccessibleAfterFirstUnlock                  7
                kSecAttrAccessibleAlways                            8
                kSecAttrAccessibleWhenUnlockedThisDeviceOnly        9
                kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly    10
                kSecAttrAccessibleAlwaysThisDeviceOnly              11
    wrapped AES256 key 0x28 bytes  (passed to kAppleKeyStoreKeyUnwrap)
    encrypted data (AES 256 CBC zero IV)
"""
from keychain import Keychain
from crypto.gcm import gcm_decrypt
from util.bplist import BPlistReader

KSECATTRACCESSIBLE = {
    6: "kSecAttrAccessibleWhenUnlocked",
    7: "kSecAttrAccessibleAfterFirstUnlock",
    8: "kSecAttrAccessibleAlways",
    9: "kSecAttrAccessibleWhenUnlockedThisDeviceOnly",
    10: "kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly",
    11: "kSecAttrAccessibleAlwaysThisDeviceOnly"
}

class Keychain4(Keychain):
    def __init__(self, filename, keybag):
        if not keybag.unlocked:
            raise Exception("Keychain4 object created with locked keybag")
        Keychain.__init__(self, filename)
        self.keybag = keybag

    def decrypt_item(self, row):
        if row["data"] != None:
            version, clas = struct.unpack("<LL", row["data"][0:8])
            if version >= 2:
                dict = self.decrypt_blob(row["data"])
                if "v_Data" in dict:
                    dict["data"] = dict["v_Data"].data
                else:
                    dict["data"] = "-- empty --"
                dict["rowid"] = row["rowid"]
                return dict
        return Keychain.decrypt_item(self, row)

    def decrypt_data(self, data):
        data = self.decrypt_blob(data)
        if type(data) == dict:
            return data["v_Data"].data
        return data

    def decrypt_blob(self, blob):
        if blob == None:
            return ""
        
        if len(blob) < 48:
            print "keychain blob length must be >= 48"
            return

        version, clas = struct.unpack("<LL",blob[0:8])
        
        if version == 0:
            wrappedkey = blob[8:8+40]
            encrypted_data = blob[48:]
        elif version == 2:
            wrappedkey = blob[12:12+40]
            encrypted_data = blob[52:-16]
        else:
            raise Exception("unknown keychain verson ", version)
            return
        
        unwrappedkey = self.keybag.unwrapKeyForClass(clas, wrappedkey)
        if not unwrappedkey:
            print "keychain unwrap fail for item with class=%d (%s)" % (clas, KSECATTRACCESSIBLE.get(clas))
            return

        if version == 0:
            return AESdecryptCBC(encrypted_data, unwrappedkey, padding=True)
        elif version == 2:
            binaryplist = gcm_decrypt(unwrappedkey, "", encrypted_data, "", blob[-16:])
            return BPlistReader(binaryplist).parse()
