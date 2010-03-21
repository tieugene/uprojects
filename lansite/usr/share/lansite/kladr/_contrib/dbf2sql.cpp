#include <xbase/xbase.h>
#include <recode.h>

int main()
{
	char scname[11], socrname[41];
	xbShort rc,i;
	xbShort lname, fname, birthdate, amount, sw, f1, memo;
	xbULong recs;
	char *p;
	xbFloat f;

	xbXBase x;
	xbDbf MyFile( &x );
	// 1. SOCRBASE
	MyFile.OpenDatabase( "SOCRBASE.DBF" );
	rc = MyFile.GetFirstRecord(); 
	while( rc == XB_NO_ERROR )
	{
		MyFile.GetField( 1, scname );  
		MyFile.GetField( 2, socrname );  
		std::cout << " scname = " << scname << std::endl;
		rc = MyFile.GetNextRecord();
	}
}