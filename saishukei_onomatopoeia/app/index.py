from flask import Flask, render_template, request
import gensim
from pykakasi import kakasi
from sudachipy import Dictionary

app = Flask(__name__)

# SudachiPy の初期化
tokenizer_obj = Dictionary().create()

# kakasi オブジェクトを初期化
k = kakasi()

# モデルのパスを取得（os.path.dirname(__file__)は現在のスクリプトのパス）
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_dir, 'models/chive-1.2-mc5_gensim/chive-1.2-mc5.kv')

# 類似度計算用のモデルの読み込み
chive = gensim.models.KeyedVectors.load(model_path)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        input_str = request.form.get('text')

        # SudachiPy を使って単語ごとに分割
        tokens = [m.dictionary_form() for m in tokenizer_obj.tokenize(input_str)]
        results = []

        # 各単語ごとに処理
        for token in tokens:
            # 類似度が最も高い語を取得
            similar, similarity = chive.most_similar(token, topn=1)[0]

            # 類似度が最も高い語をひらがなに変換
            hiragana_text = k.convert(similar)[0]['kana']

            # 取得した文字が１文字か、それ以上かで条件分岐
            if len(hiragana_text) == 1:
                # 取得した情報が1文字の場合,その一文字を、ひらがなの状態で４文字以内で、繰り返して表示
                onomatopoeia = hiragana_text*4
            else:
                # 取得した情報が1文字以上の場合, 先頭の二文字を取得して、一度だけ繰り返して表示
                onomatopoeia = hiragana_text[:2]*2

            # 結果の出力
            results.append(f"{token}→{onomatopoeia}　similarity: {similarity:.2f}")

        return render_template('index.html', results=results)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
