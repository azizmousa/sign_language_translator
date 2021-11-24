import json
import pandas as pd
import shutil
import os

def create_video(gloss, videos_list):
    print(f"copy archive/bvh_videos/{gloss}.mp4")
    shutil.copyfile(f"archive/videos/{videos_list[0]}.mp4", f"archive/bvh_videos/{gloss}.mp4")


def get_videos_ids(json_list):
    """
    function to check if the video id is available in the dataset
    and return the viedos ids of the current instance
    
    input: instance json list
    output: list of videos_ids
    
    """
    videos_list = []    
    for ins in json_list:
        video_id = ins['video_id']
        if os.path.exists(f'archive/videos/{video_id}.mp4'):
            videos_list.append(video_id)
    return videos_list



if __name__ == "__main__":
	print("loading dataframe...")
	wlas_df = pd.read_json('archive/WLASL_v0.3.json')
	wlas_df['videos_ids'] = wlas_df['instances'].apply(get_videos_ids)
	wlas_df.drop(['instances'], inplace=True, axis=1)
	
	if not os.path.exists('archive/bvh_videos'):
	    os.makedirs('archive/bvh_videos')
	wlas_df.apply(lambda row: create_video(row['gloss'], row['videos_ids']), axis=1)
	print('DONE !!')

