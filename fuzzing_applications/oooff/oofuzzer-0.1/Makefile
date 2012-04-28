all: fuzz detailed

fuzz:
	@for p in *; \
        do \
		if [ -f $$p.report ]; \
		then \
                       	echo "$$p.report exists\n"; \
                else \
                	./run_fuzzer.pl $$p; \
		fi; \
	done

detailed:
	@for p in *; \
        do \
                if [ -f $$p.report ]; \
                then \
			if [ -f $$p.detailed ]; \
			then \
                        	echo "$$p.detailed exists\n"; \
                	else \
                        	./run_detailed.pl $$p $$p.report; \
			fi; \
                fi; \
        done
