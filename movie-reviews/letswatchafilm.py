from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)


def load_data():
    df = pd.read_csv('./data/imdb/imdb_sup.csv.zip', header=None, skiprows=1)
    del df[2]
    # ratings 5 and 6 were missing because sentiments
    df.loc[df[1] > 6, 1] -= 2
    # index start from 0
    df[1] -= 1
    df.columns = ["text", "labels"]
    return df


def model_config(m):
    conf_opts = {
        # OK - slow af ~ 3h, not completed
        'xlnet1': ['xlnet', 'xlnet-large-cased', 2],
        # untested
        'xlnet2': ['xlnet', 'xlnet-base-cased', 16],
        # OK - not bad ~ 1h / epoch, not completed
        'roberta1': ['roberta', 'roberta-large', 4],
        # untested
        'bert1': ['bert', 'bert-base-cased', 16],
        # might be worth trying
        # could give us an advantage on non-english
        'xlmr1': ['xlmroberta', 'xlm-roberta-base', 16],
        'xlmr2': ['xlmroberta', 'xlm-roberta-large', 16],
        # for a speed test?
        'dbert1': ['distilbert', 'distilbert-base-multilingual-cased', 16],
        'dbert2': ['distilbert', 'distilroberta-base', 16],
        'dbert3': ['distilbert', 'distilgpt2', 16],
    }
    return conf_opts[m]


def main():
    # model = ClassificationModel("roberta", "outputs-roberta1")
    # preds = model.predict([
    #     "So much talent. So little result.",
    #     "Really disappointed at yet another dreadful script for one of my favourite books.  Badly cast, stupid additions, (a stray dog???) really just hopeless.   Is no-one brave enough to stick to the story, the characters, and wonderful dialogue from this rich and beautiful story book?",
    #     "I really love Christiana Ricci, but this is a low budget dud. The story is completely nonsensical, the CGI effects would have been cheesey in 1998 and the writing is just abismal. C Ric is charming and flawless as always, but that's all that this cinematic mess has going for it.",
    #     "Could be a good movie - but it got knocked out in the 50th minute - better things to do with my life ... ",
    #     "feels like they were trying so hard to make a second equalizer they didn't think of good story or characters before they did it. No where near as good as first movie",
    #     "Being a huge metal fan, I was excited about this movie and thought they really couldnt do much to turn me off from liking it. I was wrong. The movie is campy as hell, the dialogue is laughable about 80% of the time and the plot is hardly developed. The script writer shouldve been fired. Andy Biersack's acting shows signs of being solid in the future but ultimately hes only there to draw in a fan girl audience and the movie does nothing to hide that fact. The shining element of the movie are Remington Leith's vocal parts in my opinion. If you want a cheesy metal movie you can laugh at then here it is but if you want a deep gritty portrayal of the scene and music industry youll be mad at yourself for thinking this movie could deliver. Its not to be taken seriously which makes me think it did far more damage to the metal scene than good.",
    #     "This film was doomed from the outset due to a deals for a dollar script."
    # ])
    # logging.log(logging.INFO, str(preds))
    # exit()
    # Preparing train data

    train_df, eval_df = train_test_split(load_data())
    use_conf = 'xlnet1'
    m, pt, bs = model_config(use_conf)

    # Optional model configuration
    # For xlnet large batch size max is 2
    model_args = ClassificationArgs(num_train_epochs=2,
                                    overwrite_output_dir=True,
                                    train_batch_size=bs)
    # model_args.weight_decay = 0.01
    model = ClassificationModel(m,
                                pt,
                                num_labels=8,
                                use_cuda=True,
                                args=model_args)
    # Create a ClassificationModel
    # model = ClassificationModel('roberta',
    #                             'roberta-base',
    #                             num_labels=10,
    #                             use_cuda=True,
    #                             args=model_args)

    # model = ClassificationModel('bert',
    #                             'bert-base-cased',
    #                             num_labels=10,
    #                             args=model_args)

    # Train the model
    model.train_model(train_df)

    # Evaluate the model
    result, model_outputs, wrong_predictions = model.eval_model(eval_df)


def eval_local():
    train_df, eval_df = train_test_split(load_data())
    model = ClassificationModel("xlnet", "outputs/checkpoint-18750-epoch-1")
    result, model_outputs, wrong_predictions = model.eval_model(eval_df)
    logging.log(logging.INFO, str(result))
    logging.log(logging.INFO, str(model_outputs))
    logging.log(logging.INFO, str(wrong_predictions))


if __name__ == "__main__":
    eval_local()
    #main()