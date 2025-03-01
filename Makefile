# Convert all yaml files to pdf using typst

INVOICE_DIR = ~/Documents/invoices

%.pdf: %.yaml
	# First symlink the yaml to metadata.yaml
	ln -sf $< metadata.yaml
	# Then run typst to output the pdf
	typst compile main.typ $@


last: $(shell ls $(INVOICE_DIR)/*.yaml | tail -n 1 | sed 's/yaml/pdf/')
	@echo "Last invoice is $<"
