dictList=(acc ae ap ap90 ben bhs bop bor bur cae ccs gra gst ieg inm krm mci md mw mw72 mwe pd pe pgn pui pw pwg sch shs skd snp stc vcp vei wil yat lan armh)
for Val in "${dictList[@]}"
do
	echo 'Started' $Val 'handling'.
	python2 json_from_babylon.py $Val
done

