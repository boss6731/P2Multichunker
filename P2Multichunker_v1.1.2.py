import json, sys
import os,subprocess
from os.path import join
from os import system
import time

class Controle:
    data ={}
    global target_folders 
    global file_types
  

    target_folders = [ "materials", "models", "particles", "scenes","sound","resource" ]
    ext = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]
    file_types = ["vmt", "vtf", "mdl", "phy", "vtx", "vvd", "pcf", "vcd","wav","mp3","res"]

    
    def menu(self):
        txt = """
P2Multichunker：一個簡單的工具，將您的 mod 資產打包到適當的細分 vpk 中。

         ==說明==

         a)-將可執行檔放在 mod 目錄下，其中包含「materials」、「models」、
         “聲音”等資料夾位於其中。
         b)-設定您的 vpk 路徑（選項 1），預設通常位於：
             Windows 64 位元 C:\Program Files (x86)\Steam\steamapps\common\<GAME>\\bin
             Windows 32 位元 C:\Program Files\Steam\steamapps\common\<GAME>\\bin
         c)-執行 P2Multichunker（選項 2）並等待流程完成。

         選項 3：僅產生回應文件，這是一個 txt 文件，其中包含您的所有資訊的列表
         非 vpk 打包資產。
        
         選項 4：更改產生的 vpk 檔案的前綴，預設為「pak01」。

         選項 5：管理將掃描以包含在回應檔案中的副檔名。
         （為了方便處理問題，每次開啟程式時都會重置）

         選項
             1-VPK.exe路徑
             2-執行 P2Multichunker
             3-僅產生響應文件
             4-更改 .vpk 檔案前綴。
             5-管理擴展
             6-退出
         輸入數字：
        """
        opcao = int(input(txt))
        return opcao
    
    def main(self):
        system('cls')
        opcoes = {1:self.opcao1,2:self.p2_multichunk,3:self.createResponsefile,4:self.changeprefix,5:self.submenu_choices}
        while True:
            try:
                opcao = self.menu()
            except ValueError:
                system('cls')
                print("輸入無效\n")
                opcao = self.menu()
                
            if opcao in opcoes:
                opcoes[opcao]()
            else:
                if opcao == 6:
                    break
                else:
                    print("無效選項")
                    
    def submenu_title(self):
        txt ="""
        選擇一個選項來新增或刪除文件
         該程式將掃描並包含在您的回應檔案中.
        ---------------------------------------------------------------
        MATERIALS |MODELS   |PARTICLES |SCENES  |SOUNDS  |CONFIG. FILES
        ---------------------------------------------------------------
        0).vmt    |2).mdl   |6).pcf    |7).vcd  |8).wav  |10).res
        1).vtf    |3).phy   |          |        |9).mp3  | 
                  |4).vtx   |          |        |        | 
                  |5).vvd   |          |        |        |
        ---------------------------------------------------------------
                                    CONFIGS
        ---------------------------------------------------------------
        11) 重置搜尋參數
        12) 返回

       選擇選項： 
        """
        print("目前搜尋參數")
        print(file_types)
        opcao = int(input(txt))
        return opcao
        
    #處理回應檔案/vpk 中包含的文件
    def submenu_choices(self):
        system('cls')
        while True:
            try:
                opcao = self.submenu_title()
            except ValueError:
                system('cls')
                print("輸入無效\n")
                opcao = controle.submenu_choices()
                
            if opcao > 12:
                print("無效選項\n")
                self.submenu_choices()
            else:
                typec = self.switch(opcao)   
                if typec in self.ext:
                    if typec in file_types:
                        system('cls')
                        file_types.remove(typec)
                        print ("\n."+typec +"已從搜尋中刪除\n")     
                    else:
                        system('cls')
                        file_types.append(typec)
                        print ("\n."+typec +"已加入搜尋\n")
                        
                if opcao == 11 and len(file_types) < 11:
                    file_types.clear()
                    for x in range(0,10):
                        file_types.append(self.switch(x))
                    print ("重置完成")
                    self.submenu_choices()
                if opcao == 12:
                    controle.main()
                
    def switch(self,op):
        switcher ={
            0:"vmt", 1:"vtf", 2:"mdl", 
            3:"phy", 4:"vtx", 5:"vvd", 
            6:"pcf", 7:"vcd", 8:"wav",
            9:"mp3", 10:"res",
        }
        return switcher.get(op)

    #處理 VPK 路徑變更
    def opcao1(self):
        system('cls')
        print("您目前的路徑是: ")
        print(self.get_path()+"\n")
        choice = input("您想更新 y/n 嗎？: ")
        if choice == 'y' or choice == 'Y':
            controle.data_insert("vpk_路徑","")
            txt = """輸入VPK路徑:"""
            vpk_path = input(txt)
            isFile = os.path.isdir(vpk_path)
            if isFile == True:
                vpk_path = vpk_path.replace('\\','\\')
                vpk_path = vpk_path+'\\vpk.exe'
                print (vpk_路徑)
                controle.data_insert("vpk_path",vpk_path)
                controle.data_check("vpk_path")
            else:
                print("\n")
                print("找不到 VPK.exe: "+vpk_path)
                print("請檢查拼字錯誤或插入有效目錄")
                print("例如：C:\Program Files (x86)\Steam\steamapps\common\Portal 2\\bin")
                print("\n")
                controle.opcao1()
        else:
            controle.main()
            
    #將資料插入 VPK    
    def data_insert(self,type,path):
        controle.data[type] = path
        with open('data.json','w') as outfile:
            json.dump( controle.data,outfile)

    #檢查檔案是否仍然存在並從中獲取數據       
    def data_check(self,type):
        with open('data.json') as json_file:
            controle.data = json.load(json_file)
            text = controle.data[type]
            return text
    
    def get_path(self):
        return str(controle.data_check("vpk_path"))

    def get_prefix(self):    
        return str(controle.data_check("vpk_prefix"))

    #初步檢查文件    
    def startupCheck(self):

        if os.path.exists('data.json'):
            try:
                print("啟動檢查：[正在啟動]")
                time.sleep(1)
                print("當前VPK路徑: " + self.get_path())
                print("當前 VPK 前綴: " + self.get_prefix())
                print("啟動檢查：[確定]")
                time.sleep(2)
                controle.main()
            except (ValueError,KeyError):
                print("啟動檢查：[失敗]")
                time.sleep(1)
                print("儲存文件損壞，重新啟動... \n")
                os.remove('data.json')
                time.sleep(2)
                controle.startupCheck()
                
        else:
            print("啟動檢查：[需要生成文件]")
            time.sleep(2)
            controle.data_insert("vpk_path","C:\\Program Files (x86)\\Steam\\steamapps\\common\\Portal 2\\bin\\vpk.exe")
            controle.data_insert("vpk_prefix","pak01")
            print("目前VPK路徑: " + self.get_path())
            print("當前 VPK 前綴: " + self.get_prefix())
            time.sleep(2)
            print("啟動檢查：[確定]")
            time.sleep(1)
            controle.main()

    #Create Responsefile, as a loose file or to be used in the creation.
    def createResponsefile(self):
        system('cls')
        print("生成：responsefile.txt")
        response_path = join(os.getcwd(),"responsefile.txt")
        out = open(response_path,'w')
        len_cd = len(os.getcwd()) + 1
        for user_folder in target_folders:
            for root, dirs, files in os.walk(join(os.getcwd(),user_folder)):
                    for file in files:
                            if len(file_types) and file.rsplit(".")[-1] in file_types:
                                    out.write(os.path.join(root[len_cd:].replace("/","\\"),file) + "\n")
        out.close()
        print("完畢")

    #處理將在生成的 VPK 檔案中使用的前綴更改
    def changeprefix(self):
        system('cls')
        print("您目前的前綴是: ")
        print(self.get_prefix()+"\n")
        choice = input("Do you wish to update y/n?: ")
        if choice == 'y' or choice == 'Y':
            txt = """Enter VPK prefix:"""
            vpk_prefix = input(txt)
            if vpk_prefix is not int or float:
                controle.data_insert("vpk_prefix",vpk_prefix)
                controle.data_check("vpk_prefix")
            else:
                print("\n")
                print( vpk_prefix + " 不是有效的前綴")
                print("請檢查拼字錯誤或插入有效的前綴")
                print("\n")
                controle.changeprefix()
         #else:
             #controle.main()

    #生成 VPK
    def p2_multichunk(self):
        system('cls')
        path = controle.data_check("vpk_路徑")
        prefix = controle.data_check("vpk_前綴")
        vpk_path = str(path)
        vpk_prefix = str(prefix)
        
        system('cls')
        print("目前搜尋參數")
        print(file_types)
        controle.createResponsefile()
        print("目前VPK路徑: " + vpk_path)
        print("當前 VPK 前綴: " + vpk_prefix)
        print("\n")

        #This section generates the batch file and executes (for some reason I could only execute the process like this)
        title_text = 'ECHO !#!#!#!#!===== 生成 VPK 檔案在完成之前不要關閉此窗口 =====!#!#!#!#! \n'
        
        directory = join(os.getcwd())
        with open(os.path.join(directory, 'packing.bat'), 'w') as OPATH:
            OPATH.writelines(['@ECHO OFF \n',title_text,'"'+vpk_path,'"'+' -M a '+vpk_prefix+' @responsefile.txt \n','pause'])
               
        response_p = join(os.getcwd(),"packing.bat")
        subprocess.call([response_p])
        os.remove("packing.bat")
        os.remove("responsefile.txt")
   

controle = Controle()
controle.startupCheck()
