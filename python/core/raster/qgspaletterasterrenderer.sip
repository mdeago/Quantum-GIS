class QgsPalettedRasterRenderer: QgsRasterRenderer
{
%TypeHeaderCode
    #include "qgspalettedrasterrenderer.h"
%End
  public:
    /**Renderer owns color array*/
    QgsPalettedRasterRenderer( QgsRasterDataProvider* provider, int bandNumber, QColor* colorArray, int nColors );
    ~QgsPalettedRasterRenderer();
    QgsRasterInterface * clone();
    static QgsRasterRenderer* create( const QDomElement& elem, QgsRasterDataProvider* provider );

    void * readBlock( int bandNo, const QgsRectangle & extent, int width, int height );

    /**Returns number of colors*/
    int nColors() const;
    /**Returns copy of color array (caller takes ownership)*/
    QColor* colors() const;

    void writeXML( QDomDocument& doc, QDomElement& parentElem ) const;

    void legendSymbologyItems( QList< QPair< QString, QColor > >& symbolItems ) const;
 };