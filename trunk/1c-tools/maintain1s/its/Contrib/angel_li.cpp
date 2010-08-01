int filelen=infodatfile.GetLength();
//Номер
ИТС=filelen/1000-750;
//получаем
АдресКлюча = Адрес+"auth.asp?"+"its="+ИТС

Ключ = f(АдресКлюча)
//закачка
Адрес+"getfile.asp?addr="+АдресКлюча+"&d="+Ключ+"&its="+ИТС+"&dir="+КаталогКонф+"&file="+ИмяФайлаВерсий



//а это алгоритм получения Ключа по Index'у, т.е. АдресКлюча

CFile infodatfile;
if(!infodatfile.Open("C:\info.dat",CFile::modeRead|CFile::shareDenyNone|CFile::typeBinary))
       return false;
int filelen=infodatfile.GetLength();
int mask[16]={23,1,24,10,22,4,6,9,14,24,11,13,15,1,22,3};
mask[1]+=filelen/1000;
UCHAR block[16];
infodatfile.Seek(Index,CFile::begin);
if(infodatfile.Read(block,16)==16)
{
       for(int i=0;i<16;i++)
       {
               int val;
               if(i==1)
                       val=block[0]+mask[i];
               else
                       val=block[i]+mask[i];
               Key+=(char)(((val-1)%26)+65);
       };
};
infodatfile.Close();
