## Enhancing abstractive text summarization using an extractive layer
### Amit-Dharmadhikari, Sakshi-Gupta and Shoaib-Sheriff

<br>
This project aims to tackle the task of Summarization. Extractive summarization is wherein, sentences are ranked in terms of their importance and for the summary, top k sentences are picked. No actual generation is performed.
In abstractive summarization, the summarization process is more human-like. The encoder reads through all the sentences and then, generates a summary. Thus, the summary may have words not in original document.
<br>
<br>
In this project, we try to use extractive summarization to make abstractive summarization better. 
<br>

Requirements ############################<br>
A ROUGE environment setup. Instructions are found [here](https://poojithansl7.wordpress.com/2018/08/04/setting-up-rouge/).

This readme is divided in to 5 main parts - Dataset, Code, Run instructions, Samples and Contribution.

1. CNN/Dailymail datatset : The dataset consists of news stories from cnn and dailymail. It is created by GoogleBrain. Download [here](https://cs.nyu.edu/~kcho/DMQA/). For this project, we only consider the cnn stories. Since we use extractive summarization, we filter out stories less than 20 sentences long. The code for filtering is [here](https://github.com/ShoaibSheriff/NLP/blob/master/Project/Filter_cnn_story.ipynb)

2. Code : This part is further divided in to 3 parts - <br>
<br>
2.1. Extractive summarization - For extractive summarization, we use the text-rank algorithm. It is a page-rank based algorithm, which uses sentence similarity as the weight of the connections between each nodes. A single sentence is represented by word count occurence.

The code can be found [here](https://github.com/ShoaibSheriff/NLP/blob/master/Project/Extractive_Summarization_NER.ipynb). Using this algorithm, the key sentences have higher scores. 

2.2. Named Entity Recognition - The top sentences and importances are obtained from above. We pass every sentence in to a Named Entity Recognizer. We choose spacy for this. For every sentence, we divide its score equally among all its entities. Each entity may have more than a single score, since it can occur in multiple sentences. we save this data to be later used in the abstractive network. Again, the code for this can be found [here](https://github.com/ShoaibSheriff/NLP/blob/master/Project/Extractive_Summarization_NER.ipynb)

2.3. Abstractive summarization - The network used is based out of pointer-generator network found [here](https://github.com/becxer/pointer-generator)

Some important files are below :<br>
a. __run_summarization.py__ - This is the main interface for the code. It takes in paramters like path for stories(in the form of ".bin" files), ".imp" files from earlier step, vocabulary file, batch_size, maximum_decoder_steps etc.<br>
b. __model.py__ - This contains the definition of the encoder and decoder. Here in, we use the NER data for every summary to aid in the probability distribution of the files.<br>
c. __attention_decoder.py__ - This contains the definition to calculate attention mechanism and therby, generate the state vector.<br>
d. __batcher.py__ - Data preprocessing <br>
e. __data.py__ - Data manipulation operations

3. To run, use following steps : <br>
- Download the datatset from the given link.
- Run the filtering code to eject short stories
- Run Extractive Summarization. This generates a corresponding file for every original story and a 'imp' file which has information about the entities.
- Convert the story files to binary files by using [this](https://github.com/ShoaibSheriff/NLP/blob/master/Project/make_datafiles_for_pgn-master/make_datafiles.py) file. Sample command is :
```console
python make_datafiles.py  ./stories  ./output
```
- Train the abstractive network
```console
python run_summarization.py --mode=train --data_path=/path/to/chunked/train_* --vocab_path=/path/to/vocab --log_root=/path/to/a/log/directory --exp_name=experiment_name --max_enc_steps=/max/words/n/sentence --max_dec_steps=/max/words/to/generate --ner_path=/path/to/imp/folder 
```
- Use trained model to generate summary for test set 
```console
python run_summarization.py --mode=decode --data_path="/path/to/chunked/test_*"  --vocab_path=vocab --log_root=/path/to/log/directory --exp_name=/same/as/used/to/train --max_enc_steps=/max/words/n/sentence --max_dec_steps=/max/words/to/generate  --coverage=1 --single_pass=1 --max_dec_steps=/max/words/to/generate --ner_path=/path/to/imp/folder
```

4. Samples - Tranformations for a single story are shown below <br><br>
__Original Story__ <br>
```shell
(CNN) -- Former Illinois congressman Dan Rostenkowski, who rose through the ranks of Chicago's rough-and-tumble political scene to become one of the most powerful men on Capitol Hill, has died, according to the office of Chicago Alderman Richard Mell.

He was 82. He died in Wisconsin after an extended illness, Mell's office said.

Rostenkowski first entered Congress in 1959, during the second half of the Eisenhower administration. Known for his booming voice and reputation as a power broker, he became chairman of the tax-writing Ways and Means Committee in 1981.

During his tenure as chairman, the powerful Democrat played a key role in passing major reforms of both Social Security and the tax code, among other things.

Read more about Rostenkowski's life and career

In 1988, Rostenkowski helped pass a controversial expansion of Medicare designed to protect seniors against catastrophic medical expenses. Senior citizens became livid over the higher monthly premiums and surtax tied to the bill. The measure was repealed a year later.

Rostenkowski was defeated in the Republican landslide of 1994, however, after becoming mired in scandal. Among other things, prosecutors alleged he used public funds for personal matters and to pay employees who did little actual work.

Rostenkowski pleaded guilty to corruption charges in April 1996, and ultimately served over a year in federal prison. He was pardoned by President Bill Clinton in 2000.

"Dan Rostenkowski devoted his life to his community, Chicago and the state," Illinois House Speaker Michael Madigan said Wednesday.

"His efforts on behalf of the regular people who needed a friend to wade through the tangle of government are unparalleled."

CNN's Charles Riley contributed to this report
````
<br><br>
__Top sentences as ranked by Extractive Summarization__ <br>

```shell
He was 82. He died in Wisconsin after an extended illness, Mell's office said.

Rostenkowski first entered Congress in 1959, during the second half of the Eisenhower administration. Known for his booming voice and reputation as a power broker, he became chairman of the tax-writing Ways and Means Committee in 1981.

During his tenure as chairman, the powerful Democrat played a key role in passing major reforms of both Social Security and the tax code, among other things.

Rostenkowski was defeated in the Republican landslide of 1994, however, after becoming mired in scandal. Among other things, prosecutors alleged he used public funds for personal matters and to pay employees who did little actual work.

"Dan Rostenkowski devoted his life to his community, Chicago and the state," Illinois House Speaker Michael Madigan said Wednesday.

"His efforts on behalf of the regular people who needed a friend to wade through the tangle of government are unparalleled."
```

<br><br>

__Entities file__ <br>
```shell
Illinois 0.02792855896910068
Chicago 0.03664703938411899
Mell 0.05163371105365548
Rostenkowski 0.17407561336610938
Capitol 0.008718480415018309
Hill 0.008718480415018309
Richard 0.008718480415018309
CNN 0.060873060098733
Dan 0.02792855896910068
Wisconsin 0.042915230638637177
82 0.042915230638637177
Security 0.049899786376719
Social 0.049899786376719
Democrat 0.049899786376719
Michael 0.019210078554082372
House 0.019210078554082372
Wednesday 0.019210078554082372
Madigan 0.019210078554082372
Riley 0.052154579683714695
Charles 0.052154579683714695
````
<br><br> 
__Ground truth summary__ <br>
````shell
rostenkowski first entered congress in 1959 .
he became chairman of the tax-writing ways and means committee in 1981 .
rostenkowsi was defeated in the republican landslide of 1994 .
````

<br><br> 
__Baseline model summary__ <br>
````shell
former illinois congressman dan rostenkowski died in wisconsin after an extended illness .
he died in wisconsin after an extended illness .
he helped pass a controversial expansion of medicare designed to protect seniors against catastrophic medical expenses .
````

<br><br> 
__Proposed model summary__ <br>
````shell
rostenkowski was defeated in the republican landslide of 1994 .
he died in wisconsin after an extended illness , mell 's office said .
rostenkowski was chairman of the tax-writing ways and means committee in 1981 .
````
<br><br>
All stories can be downloaded here: <br>
[Original Stories](https://drive.google.com/file/d/1qy6c-SmiPOEmzGC_UTqv9x1fMsL1rd82/view?usp=sharing) <br>
[Top ranked sentences](https://drive.google.com/file/d/12q1QKpE9ZDEfGml37sj2ZtZoTHF9wVE3/view?usp=sharing) <br>
[NER files](https://drive.google.com/file/d/1lYEi1zHdZXAx4CjWP8-Kv0dZgBfutOXY/view?usp=sharing) <br>
[Ground-Truth Summaries](https://drive.google.com/file/d/1PQYkes8IaqimxIy3Gzlc5ZNcemd5_BOJ/view?usp=sharing) <br>
[Baseline-model Summaries](https://drive.google.com/file/d/1BboFkG4WeQ_VAjbEu96PKM9oNt9L2nVI/view?usp=sharing) <br>
[Proposed-model Summaries](https://drive.google.com/file/d/1qy6c-SmiPOEmzGC_UTqv9x1fMsL1rd82/view?usp=sharing)

5. Contribution
**ALL FILES WHICH HAVE BEEN EDITED ARE below :** <br>
a. Filter_cnn_story.ipynb - original <br>
b. Extractive_Summarization_NER.ipynb - original <br>
c. run_summarization.py, model.py, attention_decoder.py, batcher.py, data.py- cloned from Pointer Generator repository <br>
