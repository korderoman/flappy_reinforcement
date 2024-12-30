config = {'train': True,  # train or run the model
          'show_game': False,  # when training/evaluating it is much faster to not display the game graphics
          "is_manual": False,
          'print_score': 100,  # print when a multiple of this score is reached
          'max_score': 1000,  # end the episode and update q-table when reaching this score
          'resume_score': 100,  # if dies above this score, resume training from this difficult segment
          }
