/*
 faxsplit.cpp - Splits long fax into pages.
*/

#include "stdlib.h"
#include "string.h"
#include "tiffio.h"

#define	CopyField(tag, v) \
    if (TIFFGetField(in, tag, &v)) TIFFSetField(out, tag, v)

static void	cpTag(TIFF* in, TIFF* out, uint16 tag, TIFFDataType type) {
	switch (type) {
	case TIFF_SHORT:
		uint16 shortv;
		CopyField(tag, shortv);
		break;
	case TIFF_LONG:
		uint32 longv;
		CopyField(tag, longv);
		break;
	case TIFF_RATIONAL:
		float floatv;
		CopyField(tag, floatv);
		break;
	default:
		;
	}
}

static struct cpTag {
	uint16	tag;
	TIFFDataType type;
} tags[] = {
	{ TIFFTAG_IMAGEWIDTH,		TIFF_LONG },
	{ TIFFTAG_BITSPERSAMPLE,	TIFF_SHORT },
	{ TIFFTAG_COMPRESSION,		TIFF_SHORT },
	{ TIFFTAG_PHOTOMETRIC,		TIFF_SHORT },
	{ TIFFTAG_FILLORDER,		TIFF_SHORT },
	{ TIFFTAG_SAMPLESPERPIXEL,	TIFF_SHORT },
	{ TIFFTAG_PLANARCONFIG,		TIFF_SHORT },
	{ TIFFTAG_GROUP3OPTIONS,	TIFF_LONG },
	{ TIFFTAG_ORIENTATION,		TIFF_SHORT },
	{ TIFFTAG_XRESOLUTION,		TIFF_RATIONAL },
	{ TIFFTAG_YRESOLUTION,		TIFF_RATIONAL },	// 1
	{ TIFFTAG_RESOLUTIONUNIT,	TIFF_SHORT },		// 2
};
#define	NTAGS	(sizeof (tags) / sizeof (tags[0]))

int main(int argc, char *argv[])
{
	TIFF	*in = TIFFOpen(argv[1], "r");
	char	*outname = (char *) malloc(strlen(argv[1]) + 4);
	if (in && outname) {
		uint32		imagelength, outrow = 0, outcounter = 0, maxoutlen = 0;
		float		yres;
		uint16		resunit;

		TIFFGetField(in, TIFFTAG_IMAGELENGTH, &imagelength);
		TIFFGetField(in, TIFFTAG_YRESOLUTION, &yres);
		TIFFGetField(in, TIFFTAG_RESOLUTIONUNIT, &resunit);
		switch (resunit) {
			case RESUNIT_NONE:
				fprintf(stderr, "Resolution untis not defined\n");
				return (1);
				break;
			case RESUNIT_INCH:
				maxoutlen = (uint32) (11.7 * yres);	// A4
				break;
			case RESUNIT_CENTIMETER:
				maxoutlen = (uint32) (29.7 * yres);	// A4
				break;
		}
		if (maxoutlen < imagelength) {
			TIFF		*out = NULL;
			tdata_t buf = _TIFFmalloc(TIFFScanlineSize(in));
			for (uint32 row = 0; row < imagelength; row++, outrow++) {
				// 1. through close
				if (outrow == maxoutlen) {
					TIFFClose(out);
					out = NULL;
					outrow = 0;
					outcounter++;
				}
				// 2. open if need
				if (!out)	{	// new
					sprintf(outname, "%s.%03d", argv[1], outcounter);
					out = TIFFOpen(outname, "w");
					if (!out) {
						fprintf(stderr, "Can't open %s\n", outname);
						return (1);
					}
					for (struct cpTag* p = tags; p < &tags[NTAGS]; p++)	// TIFFTAG_IMAGELENGTH & TIFFTAG_ROWSPERSTRIP set automatic
						cpTag(in, out, p->tag, p->type);
				}
				// 3. main
				TIFFReadScanline(in, buf, row);
				TIFFWriteScanline(out, buf, outrow);
			}
			_TIFFfree(buf);
			TIFFClose(out);
		}
		TIFFClose(in);
	}
}
