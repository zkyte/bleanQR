


class GenerateVCF:

    def __init__(self, data, file_path):
        self.data = data
        self.file_path = file_path
        

    def generateVCFString(self):
        with open(self.file_path, "w") as file:
            file.write('BEGIN:VCARD \n')
            file.write('VERSION:3.0 \n')
            if self.data.get("dname", "") != "":
                file.write('FN;CHARSET=UTF-8:' + str(self.data.get("dname", "")) + '\n')
            if self.data.get("name", "") != "":
                file.write('N;CHARSET=UTF-8:J' + str(self.data.get("name", "")) + ';;;\n')
            if self.data.get("email", "") != "":
                file.write('EMAIL;CHARSET=UTF-8;type=HOME,INTERNET: ' + str(self.data.get("email", "")) + '\n')
            if self.data.get("image", "") != "":
                file.write('PHOTO;ENCODING=b;TYPE=image/jpeg:' + str(self.data.get("image", "")) + '\n')
            if self.data.get("phone", "") != "":
                file.write('TEL;TYPE=CELL:' + str(self.data.get("phone", "")) + '\n')
            if self.data.get("address_1", "") != "":
                file.write('LABEL;CHARSET=UTF-8;TYPE=HOME:' + str(self.data.get("address_1", "")) + '\n')
            if self.data.get("address_2", "") != "":
                file.write('ADR;CHARSET=UTF-8;TYPE=HOME:' + str(self.data.get("address_2", "")) + '\n')
            if self.data.get("role", "") != "":
                file.write('ROLE;CHARSET=UTF-8:' + str(self.data.get("role", "")) + '\n')
            if self.data.get("company", "") != "":
                file.write('ORG;CHARSET=UTF-8:'+ str(self.data.get("company", "")) + '\n')
            if self.data.get("url", "") != "":
                file.write('URL;CHARSET=UTF-8:' + str(self.data.get("url", ""))+ '\n')
            if self.data.get("remark", "") != "":
                file.write('NOTE;CHARSET=UTF-8:' + str(self.data.get("remark", "")) + '\n')
        
            file.write('REV:2022-04-25T11:14:24.064Z \n')
            file.write('END:VCARD')




