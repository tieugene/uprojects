#include "catmd.h"

#include <zlib.h>

const int iMulter = 200;

int	unpack_data(Pdata &in, Pdata &out) {
	BYTE	*tmp;
	int	err;

	out.size = in.size * iMulter;
	tmp = (BYTE *) malloc (in.size + 2);	// !!! new = Seg fault !!!
	out.data = (BYTE *) malloc (out.size);	// !!! new = Seg fault !!!
	if (!(tmp) || !(out.data)) {
		out.size = 0;	// "Out of memory"
		return (1);
	}
	tmp[0] = 'x';
	tmp[1] = '^';
	memcpy(tmp + 2, in.data, in.size);
	err = data_inflate(tmp, in.size + 2, out.data, &out.size);
	delete tmp;

	if(err)	{	// error - data isn't unpacked
		out.size = 0;
		delete out.data;
		return (2);
	} else
		return (0);
}

#define	CHECK_ERR(err, msg) { if (err != Z_OK) { cerr << msg << "error: " << err << endl; return(-1); } }
int	data_inflate(BYTE *src, DWORD srclen, BYTE *dst, DWORD *dstlen)	// 0 = OK, -1 = err
{
	z_stream	d_stream;
	int		err;
	
	d_stream.next_in  = src;
	d_stream.avail_in = (uInt)srclen;
//	d_stream.avail_in = 0; // ?
	
	d_stream.next_out = dst;
	d_stream.avail_out = (uInt)*dstlen;

	d_stream.zalloc = (alloc_func)0;
	d_stream.zfree = (free_func)0;
//	d_stream.opaque = (voidpf)0;

	err = inflateInit(&d_stream);
	CHECK_ERR(err, "inflateInit");
	
	err = inflate(&d_stream, Z_FINISH);

//	while (d_stream.total_out < *dstlen && d_stream.total_in < srclen) {
//		d_stream.avail_in = d_stream.avail_out = 1; /* force small buffers */
//		err = inflate(&d_stream, Z_NO_FLUSH);
//		if (err == Z_STREAM_END) break;
//			CHECK_ERR(err, "inflate");
//	}
	*dstlen = d_stream.total_out;

	err = inflateEnd(&d_stream);
	CHECK_ERR(err, "inflateEnd");
	return(0);
}
