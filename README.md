# Gwoyeu-Romatzyh-Converter
A Python function to convert standard Hanyu Pinyin input into the deprecated tonal spelling system of [Gwoyeu Romatzyh](https://en.wikipedia.org/wiki/Gwoyeu_Romatzyh) (GR, 國語羅馬字).

### Use

Gwoyeu Romatzyh is a now-outmoded romanization standard for Modern Standard Chinese, and one where the differences in the four tones would be indicated by the spelling of the syllables instead of numbers or diacritics. For example:

1. 媽 (PY: *mā*, GR: *mha*)
2. 麻 (PY: *má*, GR: *ma*)
3. 馬 (PY: *mǎ*, GR: *maa*)
4. 罵 (PY: *mà*, GR: *mah*)

More information on the complex rules GR uses can be found on [Wikipedia here](https://en.wikipedia.org/wiki/Spelling_in_Gwoyeu_Romatzyh). 

This function accepts Hanyu Pinyin (PY) syllables in numerical form (e.g. *pin1 yin1*), which can then be converted into GR. The function is meant to work with a tokenizer like **[mafan](https://github.com/hermanschaaf/mafan)** and as such will treat multiple syllables as a single word-unit, including some of the GR abbreviations. For example:

* 漢語 (PY: *Hàn​yǔ*, GR: *hannyeu*)
* 高興 (PY: *gāo​xìng​*, GR: *gaushinq*)
* 銀河 (PY: *yín​hé​*, GR: *ynher*)
* 國家安全 (PY: *guó​jiā​'ān​quán*, GR: *gwojiaanchyuan*)
* 椅子 (PY: *yǐ​zi​*, GR: *yez*)
* 每個 (PY: *měi​ge​*, GR: *meeig*)

### Note

The function does not apply the even-more complex spelling rules that form rhotacization (兒化).
