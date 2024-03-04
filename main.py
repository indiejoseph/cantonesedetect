import re

# Cantonese characters not found in Mandarin
canto_unique = re.compile(
    r"[嘅嗰啲咗佢喺咁噉冇啩哋畀嚟諗惗乜嘢閪撚𨳍𨳊瞓睇㗎餸𨋢摷喎嚿噃嚡嘥嗮啱揾搵喐逳噏𢳂岋糴揈捹撳㩒𥄫攰癐冚孻冧𡃁嚫跣𨃩瀡氹嬲掟孭黐唞㪗埞忟𢛴]|"
    + r"唔[係得會好識使洗駛通知到去走掂該錯差]|點[樣會做得解]|[琴尋噚聽第]日|[而依]家|家[下陣]|[真就實梗又話都]係|邊[度個位科]|"
    + r"[嚇凍攝整揩逢淥浸激][親嚫]|[橫搞傾諗得唔]掂|仲[有係話要得好衰唔]|返[學工去歸]|執[好生實返輸]|[留坐剩]低|"
    + r"屋企|收皮|慳錢|傾[偈計]|幫襯|求其|是[但旦]|[濕溼]碎|零舍|肉[赤緊酸]|核突|同埋|勁[秋抽]"
)
# Cantonese characters that are less common in Mandarin
canto_feature = re.compile(r"[係唔]")
# A list of exceptions where the above characters can be found in Mandarin
canto_exclude = re.compile(r"(關係|吱唔|咿唔)")

# Mandarin characters that are less common in Cantonese
swc_feature = re.compile(r"[那是的他它吧沒麼么些了卻説說吃弄]|而已")

# A list of exceptions where the above characters can be found in Cantonese (mainly phrases or proper nouns)
swc_exclude = re.compile(
    r"亞利桑那|剎那|巴塞羅那|薩那|沙那|哈瓦那|印第安那|那不勒斯|支那|"
    + r"是[否日次非但旦]|[利於]是|唯命是從|頭頭是道|似是而非|自以為是|俯拾皆是|撩是鬥非|莫衷一是|唯才是用|"
    + r"[目綠藍紅中]的|的[士確式]|波羅的海|眾矢之的|的而且確|大眼的度|"
    + r"些[微少許小]|"
    + r"[淹沉浸覆湮埋沒出]沒|沒[落頂收]|神出鬼沒|"
    + r"了[結無斷當然哥結得解事之]|[未明]了|不得了|大不了|"
    + r"他[信人國日殺鄉]|[其利無排維結]他|馬耳他|他加祿|他山之石|"
    + r"其[它]|"
    + r"[酒網水貼]吧|吧[台臺枱檯]|"
    + r"[退忘阻]卻|卻步|"
    + r"[遊游小傳解學假淺眾衆訴論][説說]|[說説][話服明]|自圓其[説說]|長話短[說説]|不由分[說説]|"
    + r"吃[虧苦力]|"
    + r"弄[堂]"
)
# A list of quotes: Content inside and outside a pair of quotes should be treated separately.
allquotes = re.compile(r"「[^「」]*」")

# A list of sentential delimiters
alldelimiters = re.compile(r"，。；？！⋯")


def count_canto_feature(sentence):
    """
    Get the number of Cantonese features
    """
    return len(re.findall(canto_feature, sentence)) - len(
        re.findall(canto_exclude, sentence)
    )


def count_swc_feature(sentence):
    """
    Get the number of Mandarin features
    """
    return len(re.findall(swc_feature, sentence)) - len(
        re.findall(swc_exclude, sentence)
    )


def get_sent_stat(sentence):
    """
    Get the sentence stats
    """
    num_canto_unique = len(re.findall(canto_unique, sentence))
    num_swc_feature = count_swc_feature(sentence)
    num_canto_feature = count_canto_feature(sentence)

    return num_canto_unique, num_swc_feature, num_canto_feature


def sentence_is_cantonese(sentence):
    """
    Check whether a sentence is Cantonese
    """
    num_canto_unique = len(re.findall(canto_unique, sentence))
    num_swc_feature = count_swc_feature(sentence)

    return num_canto_unique > 1 or num_swc_feature == 0


def get_document_stat(document):
    quotes = "⋯".join(re.findall(allquotes, document))
    matrix = re.sub(allquotes, " ", document)

    doc_quotes_canto_unique = len(re.findall(canto_unique, quotes))
    doc_matrix_canto_unique = len(re.findall(canto_unique, matrix))
    doc_quotes_swc_feature = count_swc_feature(quotes)
    doc_quotes_canto_feature = count_canto_feature(quotes)
    doc_matrix_swc_feature = count_swc_feature(matrix)
    doc_matrix_canto_feature = count_canto_feature(matrix)

    sents_quotes = re.findall(
        f"(?:[^{alldelimiters}]*)*[{alldelimiters}]?", quotes)
    sents_matrix = re.findall(
        f"(?:[^{alldelimiters}]*)*[{alldelimiters}]?", matrix)
    sents_quotes_canto = list(
        filter(sentence_is_cantonese, sents_quotes))
    sents_matrix_canto = list(
        filter(sentence_is_cantonese, sents_matrix))

    print(f"Document: {document[:20]} ...")
    print("Legit Cantonese ratio (by sentence)")
    print(
        f"Matrix: {len(sents_matrix_canto)}/{len(sents_matrix)} ({len(sents_matrix_canto)/len(sents_matrix)*100}%)"
    )
    if len(sents_quotes) > 0:
        print(
            f"Quotes: {len(sents_quotes_canto)}/{len(sents_quotes)} ({len(sents_quotes_canto)/len(sents_quotes)*100}%)"
        )
    print(f"Document-based metrics")
    print(
        f"[Matrix] Uniquely Cantonese: {doc_matrix_canto_unique}, Mandarin Features: {doc_matrix_swc_feature}"
    )
    print(
        f"[Quotes] Uniquely Cantonese: {doc_quotes_canto_unique}, Mandarin Features: {doc_quotes_swc_feature}"
    )
    if doc_matrix_swc_feature <= 3 and doc_matrix_canto_unique > 1:
        print("Written Cantonese")
    elif (
        doc_quotes_canto_unique > doc_matrix_canto_unique
        and doc_matrix_swc_feature > doc_matrix_canto_unique
    ):
        print("Dialogue-Narrative split")
    elif doc_matrix_swc_feature > 3 and doc_matrix_canto_unique > 1:
        print("Mixed/ Translanguaging")
    elif doc_matrix_swc_feature > 3 and doc_matrix_canto_unique == 0:
        print("SWC")
    else:
        print("Cannot be classified")


data = [
    "0 我今日第一日返工，請多多指教。",
    "1 我地今晚出去食飯。我去會合你先。你鍾意可以去剪個頭髮先，個袋我幫你keep。",
    "2 德州「鼠王」凱普林，牠的體重超過一百磅，外貌十足倉鼠，其實是一隻水豚，因身形龐大，走在街上常被人當作狗呢。",
    "3 來自南美洲的水豚是園內的明星，被日本人譽為是擁有世上最強治癒力的動物，這隻草食動物沒有攻擊性，外表儍頭儍腦，在風和日麗的早上在室外園區的草地上悠然自得",
    "4 【橋本湊水豚】當晚，阿笨主人宮澤先生在facebook貼出新相，阿笨一家三口難得同框，向觀眾道別及答謝多年來的支持。《志村動物園》結束後，下月會有同樣以動物作招徠的《I Love大家的動物園》，由嵐成員相葉雅紀繼續擔任主持，人氣女星橋本環奈會加盟，以固定陣容挑戰照顧水豚。",
    "5 全球最大嘅齧齒動物水豚以及雪白北極狐，各自圍住南瓜歡度哈囉喂。今年海洋公園哈囉喂全日祭開放到11月1日，仲餘下4個特選日子，想同動物大使一齊慶祝哈囉喂就要快啲嘞喂。",
    "6 𠵱家海洋公園有3隻水豚，一男兩女分別叫Samba、Hatoru同May。而赤掌獠狨就一族9隻天性非常八卦，有嘢食時會伸手捉住個兜睇吓有咩食，所以大家餵食時，記住唔好手多多摸佢哋。",
    "7 喺幼兒照顧方面，特區政府喺二零一八至一九年度向兒童發展基金注資三億元以幫助基層兒童，同時提升幼兒中心嘅資助水平同埋合資格人員嘅人手比例、優化「鄰里支援幼兒照顧計劃」同埋加強課餘託管服務。至於安老服務，本屆政府大幅增加資助家居照顧服務嘅服務名額、「長者社區照顧服務券試驗計劃」下嘅服務券數目、資助安老宿位，以及提升私營安老院服務嘅質素。另外，我哋已經將到校學前康復服務恆常化、豁免輪候特殊幼兒中心學習訓練津貼嘅家庭入息審查；而殘疾人士家長及親屬資源中心自二零一九年起由六間逐步增加至十九間。我哋期望透過上述措施能夠紓緩婦女作為主要家庭照顧者嘅壓力，同時可以協助釋放婦女勞動力，等佢哋可以發揮所長。",
    "8 喺小王子嘅行星上面，有一種好簡單嘅花，只有一層花瓣，佢哋一啲都唔掗埞，亦唔會麻煩到任何人。朝早嘅時候，佢哋會喺草叢中出現，然後到咗黃昏就慢慢凋謝。但有一日，唔知邊度飄咗一粒種子過嚟，喺呢度發芽。小王子好細心噉觀察呢一棵與別不同嘅幼苗，因為，佢隨時可能係一個猢猻樹嘅新品種。但係呢棵幼苗好快就冇再繼續長大，反而開始準備開花。小王子望住巨型嘅花苞成長，覺得一定會開出一朵奇妙嘅花嚟。不過朵花匿埋咗喺佢綠色嘅房間入面，花咗好多好多時間去裝扮自己。佢小心翼翼噉選擇自己嘅顏色。慢條斯理噉着上新衫，逐片逐片花瓣噉整理好。佢並唔想好似罌粟花噉，皺掹掹噉走出嚟。佢只係願意喺散發住令人驚艷嘅光芒之下出現。",
    "9 身處喺呢個工廈單位嘅理雄，忍受炎夏中冇冷氣嘅不適，正視住佢眼前嘅人。明明有求於佢，應該信任佢，但呢個叫「阿凌」嘅人實在奇怪。大熱天時，明明有裝冷氣但唔開，仲要着住長袖嘅棗紅色校服冷衫，但阿凌居然一滴汗都冇流。可能佢同香港嘅女學生一樣，返學嘅時候皮膚同件冷衫連成一體，除唔到落嚟。但阿凌點睇都至少廿二、三歲，點解仲要噉着？何況佢雖然生得好靚，但究竟係男係女，理雄都仲未搞得清楚。濃密細長嘅眼睫毛、精緻嘅五官、白晢嘅瓜子臉……但佢嘅眼神帶住一陣冷冽、配上層次感強烈嘅深棕色短髮，無論話佢係一個中性打扮嘅美女，抑或一個男生女相嘅型男，都會有人相信。",
    "10 西哥德人係嚟自巴爾幹地區嘅蠻族，喺公元四到五世紀之間，大部分時間同當時嘅羅馬帝國對立，甚至曾經攻佔羅馬城大肆劫掠，然後不斷西進，喺現今法國南部同伊比利亞半島建立西哥德王國，公元507年被法蘭克人擊敗，相繼失去首都圖盧茲同納博訥，退守伊比利亞半島，短暫定都巴塞羅那，最後喺公元542年左右遷都至托利多，一直到711年滅國為止。西哥德人原先信奉基督教亞流派，同原先定居嘅羅馬帝國子民有啲衝突。公元587年，國王帶領貴族同神職人員轉投主流天主教，為伊比利亞半島嘅主要宗教信仰奠定統一嘅基礎。喺資源有限嘅情況下，藝術當然係以宗教、崇拜為先，而且亦保存得最好。",
    "11 如果勇敢講緊嘅，係嗰種咩都唔怕嘅大無畏精神，噉可能唔係話你想學就學得嚟，更加多係天生決定究竟你有幾大膽。就正如畏唔畏高一樣，當然見得多就冇咁驚，但先天決定咗大部份你有幾畏高。但如果「勇敢」講嘅唔係會唔會驚，而係驚嘅時候有冇克服恐懼嘅能力，件事就完全唔同。點樣喺恐懼嘅心理狀態下繼續做應做之事，係一件人人皆可以學習嘅事情，我哋唔需要羨慕其他人。孟子認為「人皆可以為堯舜」，而我認為「人皆可以為勇者」。人人天賦當然係有差別，但噉理解下，勇氣唔再係可望而不可即嘅嘢，只要你想，你都可以培養自己，變成一個越嚟越勇敢嘅人。",
    "12 但點解表達情感唔可以用語言，而要用以行為為主嘅禮？我個人估嘅係，一嚟言語多修飾同大話，身體動作較難假裝；二嚟言語多牽涉思考，而身體較隨直覺而行；三嚟人比較易受人地嘅表情行為挑動情緒，而言語則較難做到呢點，就正如點解啲人演講要有埋表情動作氣氛等。呢幾點可能其實都係歸入一點：身體同情緒嘅關係大概密切過言語同情緒？另外仲有或者禮牽涉場境同器具，可以更豐富、更細膩噉表達情緒，就好似戲劇同電影做到一啲廣播劇做唔到嘅嘢？講到尾，一啲好複雜嘅禮其實同做戲飾演角色都有幾分相似，都係從外到內再到外。",
    "13 我會望見午後嘅陽光灑落喺露台邊。光線會入屋，入屋嘅角度同範圍剛剛好，唔會曬到梳化上慵懶嘅我。我會望見露台窗紗外揾緊機會衝入嚟嘅蚊，有時會發現唔覺意跟咗我入屋嘅蚊。唔知佢哋入到屋喺幸定不幸。佢哋可能有機會吸到我血，會食飽飽，但入得嚟嘅蚊九成係死路一條。我唔用電蚊拍，因為怕手腳唔協調嘅我電親自己。盡量唔會雙手拍蚊，因為會好痛，同埋成日拍唔中。我會揮掌將佢哋打暈，掌心向下噉將佢地擊落，再拎張紙温柔噉執起暈咗嘅不速之客，輕輕摙死，將死無全屍嘅佢送入垃圾桶。試過一日送咗五隻蚊歸西，而我手上一滴血都冇沾染到。",
    "14 小時候，父親假日喜帶一家大小出外，到市區離島走走是平常事，但去澳門除了他自家瞞著母親去「過大海」之外，卻是一件「大陣仗」的事——所謂「大陣仗」，去的不僅是我一家七口，還連同姑母伯父或契爺家，連我患有潔癖多年不肯出外的姑姐也曾隨行，最幼的手抱嬰最大的老祖母，一海之隔的澳門，成了幾個血脈相連的家庭出外團聚之地，最方便也可能是唯一之地。現在回想，記憶已十分模糊，在父母家的相簿想必亦早已發黃。閉目召喚殘餘印象，即時閃起的是澳門當時滿街的三輪車，我們同時僱用幾輛，車伕是司機也是一人導遊，載我們在市中心遊覽，遊了甚麼地方無法記起了，只記得他們好像都是上了年紀一身黑實踩著腳踏的腿尤其有勁。在三輪車上的我愉快嗎不記得了，如今回想只慶幸也曾搭過這種澳門「土特產」旅遊交通工具，這終歸被時代淘汰的人與物。",
    "15 駱督察吐了一口氣，心底的不安卻沒有因為這一口氣而消減半分。比起在停屍間觀看驗屍過程，這刻他的心情更是沉重。身穿整齊藍色西裝的他，落寞地瞧着病床上的人。在這間單人病房裏，病榻上躺着的，是一個龐眉皓髮的老年人。在呼吸面罩下，老人的臉上滿布皺紋，雙目緊閉，膚色蒼白，長着零星老人斑的手臂上插着細管，連接着好幾台運作中的醫療儀器。病床上方懸掛着十七吋的平面熒幕，顯示着病人的脈搏、血壓、血含氧量等資訊，線條緩慢地從右往左移動，如果這畫面不是跳動着，任誰也會覺得這老人已經死去，床上躺着的是一具保存得很好的屍體。這位老人是駱督察的「師傅」，是多年來指導他調查、搜證、推理、破案，卻從不按牌理出牌的師傅。",
    "16 難得一天假期，陳老師決定好好享受一下。一起床，她就想先到街上走走。她套上顏色亮麗的拖鞋式涼鞋，出去買報紙，買抗敏牙膏和煮好了的軟花生。她當然還要租一張影碟來看。陳老師對影碟要求不高：只要沒有大災難、故事不太繁複、沒有人會死、有一點點愛情、最後大團圓結局的就好。不知怎地，她開始教書的頭兩年，還可以看一點點沉重的東西，即使是《舒特拉的名單》之類的片子也不怕，現在竟都不敢看了，放假還要繼續接觸這些人間慘劇，會變瘋的。最後，她還必須為自己煮一鍋老火生魚湯。近來太沒精神了。父母遷回番禺以後，她一次生魚湯都未吃過。一想到那些浸透了魚肉鮮味的淮山、茨實、玉竹和蓮子，還有蘸上醬油、煮爛了的瘦豬肉，她的口水就從心底湧到舌面上來。想着想着，陳老師已快步踏進了菜市場。",
    "17 蜂類螫傷是較常見的蟲螫，螫傷的部位會疼痛、發癢及腫脹。後果一般並不嚴重，但有些人對昆蟲的毒液會產生過敏反應、過敏性休克、甚至窒息。如被紅火蟻咬傷的話，傷口則會劇痛，並可能出現嚴重過敏反應。如果傷病者嘴部被螫傷，嘴或喉部組織可能嚴重腫脹，導致呼吸道受阻。可給予傷病者吸吮冰塊或喝小口冷水預防腫脹。如果腫脹惡化，應尋求醫療援助。海洋生物的傷害可以由咬傷、螫傷或刺傷三種方式所造成。一般情況下，不會有嚴重問題。不過一些海洋生物含有毒素，例如水母、海葵、石頭魚、魔鬼魚等。如果螫或刺帶有毒液，會造成中毒，徵狀可由局部的痛楚、麻痺達至致命的程度。傷病者可能有過敏反應，例如紅腫、紅疹，更可能會休克。被一些大型魚類咬傷的傷口可以很大和深，造成嚴重創傷。海膽的刺針雖然大多數沒有毒，但傷口可能會受細菌感染。",
    "18 大佬叫我們脫下白袍，說，以後大家是兄弟，你們不要成天在酒吧睡覺打啤牌，要出去賣嘢。原來賣那啲「嘢」，是白粉。",
    "19 阿牛給我食煙，說有嘢，我就接過來食，不到幾分鐘就天旋地轉，想嘔，我就走到廁所去嘔，又沒甚麼嘔出來。出來還是好暈，阿物說，第一次是這樣。"
]

if __name__ == '__main__':
    for doc in data:
        get_document_stat(doc)
        print('*'*10)
