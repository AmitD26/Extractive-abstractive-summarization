import spacy
import os


nlp = spacy.load('en')

output_baseline = open("output_baseline_cosine.txt", "w")
output_new = open("output_new_cosine.txt", "w")
top_summaries = open("top_summaries_cosine.txt", "w")

d = dict()
	
for i in range(7054):
	f1 = open("/home/amit/Desktop/b4_________decode_test_500maxenc_4beam_35mindec_40maxdec_ckpt-238410/decoded/" + str(i).zfill(6) + "_decoded.txt")
	f2 = open("/home/amit/Desktop/aftr________decode_test_500maxenc_4beam_35mindec_40maxdec_ckpt-238410/decoded/" + str(i).zfill(6) + "_decoded.txt")
	f3 = open("/home/amit/Desktop/aftr________decode_test_500maxenc_4beam_35mindec_40maxdec_ckpt-238410/reference/" + str(i).zfill(6) + "_reference.txt")
	

	doc1 = nlp(f1.read())
	doc2 = nlp(f2.read())
	doc3 = nlp(f3.read())
	
	sim1 = doc1.similarity(doc3)
	sim2 = doc2.similarity(doc3)
	
	if sim2 > sim1:
		d[sim2 - sim1] = i

	output_baseline.write(str(sim1) + "\n")
	output_new.write(str(sim2) + "\n")
	
	f1.close()
	f2.close()
	f3.close()
	
output_baseline.close()
output_new.close()

top_summaries.write("Total number of summaries which performed better than baseline: " + str(len(d)) + "\n")

nd = sorted(d, reverse=True)[:50]
for i in nd:
	top_summaries.write(str(d[i]) + "\n")
	
top_summaries.close()
