#import "template.typ": invoice-from-metadata


#let meta = yaml("metadata.yaml")
// #meta.doc-info.insert("logo", image("logo.svg", height: 5em))
#invoice-from-metadata(meta, pre-table-body: [
    Tous les prix sont HT. TVA non applicable, art. 293 B du CGI.
], apply-default-style: true)
