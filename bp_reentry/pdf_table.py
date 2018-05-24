def listing():
    response.title = "web2py sample listing"

    # define header and footers:
    head = THEAD(TR(TH("Header 1", _width="50%"), 
                    TH("Header 2", _width="30%"),
                    TH("Header 3", _width="20%"), 
                    _bgcolor="#A0A0A0"))
    foot = TFOOT(TR(TH("Footer 1", _width="50%"), 
                    TH("Footer 2", _width="30%"),
                    TH("Footer 3", _width="20%"),
                    _bgcolor="#E0E0E0"))

    # create several rows:
    rows = []
    for i in range(1000):
        col = i % 2 and "#F0F0F0" or "#FFFFFF"
        rows.append(TR(TD("Row %s" %i),
                       TD("something", _align="center"),
                       TD("%s" % i, _align="right"),
                       _bgcolor=col)) 

    # make the table object
    body = TBODY(*rows)
    table = TABLE(*[head, foot, body], 
                  _border="1", _align="center", _width="100%")

    if request.extension == "pdf":
        from gluon.contrib.pyfpdf import FPDF, HTMLMixin

        # define our FPDF class (move to modules if it is reused frequently)
        class MyFPDF(FPDF, HTMLMixin):
            def header(self):
                self.set_font('Arial', 'B', 15)
                self.cell(0, 10, response.title, 1, 0, 'C')
                self.ln(20)

            def footer(self):
                self.set_y(-15)
                self.set_font('Arial', 'I', 8)
                txt = 'Page %s of %s' % (self.page_no(), self.alias_nb_pages())
                self.cell(0, 10, txt, 0, 0, 'C')

        pdf = MyFPDF()
        # first page:
        pdf.add_page()
        pdf.write_html(str(XML(table, sanitize=False)))
        response.headers['Content-Type'] = 'application/pdf'
        return pdf.output(dest='S')
    else:
        # normal html view:
        return dict(table=table)

listing()