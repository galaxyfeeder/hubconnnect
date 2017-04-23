package com.example.thor.copenhacks;

import android.content.Context;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;
import android.util.Pair;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.bumptech.glide.Glide;
import com.google.gson.Gson;
import com.lorentzos.flingswipe.SwipeFlingAdapterView;

import java.util.ArrayList;
import java.util.List;

import butterknife.BindView;
import butterknife.ButterKnife;

public class MainActivity extends AppCompatActivity {

    private ArrayList<Pair<String,String>> al;
    private ArrayList<String> al2;
    private MemberAdapter arrayAdapter;
    private ArrayAdapter<String> arrayAdapter2;
    private int i;
    ImageView imageView;


    @BindView(R.id.frame)
    SwipeFlingAdapterView flingContainer;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        ButterKnife.bind(this);


        imageView = (ImageView) findViewById(R.id.foto);
        /**
         Glide
         .with(MainActivity.this)
         .load("https://avatars1.githubusercontent.com/u/26429081?v\\u003d3")
         .centerCrop()
         .crossFade()
         .into(imageView);
         **/


        ArrayList<Bitmap> prova;

        arrayAdapter = new MemberAdapter(this);


        al = new ArrayList<Pair<String,String>>();
        String url = "https://copenhacks2.herokuapp.com/like";
        new HttpJson().setCallback(new HttpJson.Callback() {
            @Override
            public void onResponse(List<ServerResponse> t) {
                //String json = new Gson().toJson(t);
                al.clear();
                for (int i = 0; i < 3; ++i) {
                    String bio = t.get(i).bio;
                    String name = t.get(i).name;
                    String[] skills = t.get(i).languages;
                    String total = "   ";
                    total = total + bio + " ~\n ";
                    total = total + " Name: " + name + "\n ";
                    total = total + "  SKILLS:  ";
                    for (int k = 0; k < skills.length; ++k) {
                        total = total + " " + skills[k] + '\n';
                    }

                    al.add(Pair.create(total,t.get(i).avatar_url));



                }
                arrayAdapter.addAll(al);
                arrayAdapter.notifyDataSetChanged();
                Log.d("Main", "Server response: " + t.size());


            }
        }).execute(url);


        //arrayAdapter2 = new ArrayAdapter<>(this, R.layout.item, R.id.helloText, al);


        flingContainer.setAdapter(arrayAdapter);
        flingContainer.setFlingListener(new SwipeFlingAdapterView.onFlingListener() {
            @Override
            public void removeFirstObjectInAdapter() {
                // this is the simplest way to delete an object from the Adapter (/AdapterView)
                Log.d("LIST", "removed object!");
                try {
                    arrayAdapter.remove(0);
                    arrayAdapter.notifyDataSetChanged();
                }catch(Exception e){
                    Log.d("ERROR","I'm empty");
                }
            }

            @Override
            public void onLeftCardExit(Object dataObject) {
                //Do something on the left!
                //You also have access to the original object.
                //If you want to use it just cast it (String) dataObject
                makeToast(MainActivity.this, "Left!");
                /**
                try {
                    arrayAdapter.remove(0);
                    arrayAdapter.notifyDataSetChanged();
                }catch(Exception e){
                    Log.d("ERROR","I'm empty");
                }
                 **/
                String url = "https://copenhacks2.herokuapp.com/dislike";
                new HttpJson().setCallback(new HttpJson.Callback() {
                    @Override
                    public void onResponse(List<ServerResponse> t) {
                        //String json = new Gson().toJson(t);
                        ArrayList<Pair<String, String>> p = new ArrayList<Pair<String, String>>();
                        for (int i = 0; i < 3; ++i) {
                            String bio = t.get(i).bio;
                            String name = t.get(i).name;
                            String[] skills = t.get(i).languages;
                            String total = "   ";
                            total = total + bio + " ~\n ";
                            total = total + " Name: " + name + "\n ";
                            total = total + "  SKILLS:  ";
                            for (int k = 0; k < skills.length; ++k) {
                                total = total + " " + skills[k];
                                if (k % 3 == 0) total = total + '\n';
                            }

                            p.add(Pair.create(total, t.get(i).avatar_url));

                        }
                        arrayAdapter.addAll(p);
                        arrayAdapter.notifyDataSetChanged();
                        Log.d("Main", "Server response: " + t.get(0).avatar_url);


                    }
                }).execute(url);


            }

            @Override
            public void onRightCardExit(Object dataObject) {
                makeToast(MainActivity.this, "Right!");
                /**
                try {
                    arrayAdapter.remove(0);
                    arrayAdapter.notifyDataSetChanged();
                }catch(Exception e){
                    Log.d("ERROR","I'm empty");
                }
                 **/

                String url = "https://copenhacks2.herokuapp.com/like";
                new HttpJson().setCallback(new HttpJson.Callback() {
                    @Override
                    public void onResponse(List<ServerResponse> t) {
                        ArrayList<Pair<String, String>> p = new ArrayList<Pair<String, String>>();
                        for (int i = 0; i < 3; ++i) {
                            String bio = t.get(i).bio;
                            String name = t.get(i).name;
                            String[] skills = t.get(i).languages;
                            String total = "   ";
                            total = total + bio + " ~\n ";
                            total = total + " Name: " + name + "\n ";
                            total = total + "  SKILLS:  ";
                            for (int k = 0; k < skills.length; ++k) {
                                total = total + " " + skills[k];
                                if (k % 2 == 0) total = total + '\n';
                            }

                            p.add(Pair.create(total, t.get(i).avatar_url));

                        }
                        arrayAdapter.addAll(p);
                        arrayAdapter.notifyDataSetChanged();
                        Log.d("Main", "Server response: " + t.get(0).avatar_url);

                    }
                }).execute(url);
            }


            @Override
            public void onAdapterAboutToEmpty(int itemsInAdapter) {
                // Ask for more data here
                arrayAdapter.notifyDataSetChanged();
                Log.d("LIST", "notified");
                i++;
            }

            @Override
            public void onScroll(float scrollProgressPercent) {
                View view = flingContainer.getSelectedView();
                view.findViewById(R.id.item_swipe_right_indicator).setAlpha(scrollProgressPercent < 0 ? -scrollProgressPercent : 0);
                view.findViewById(R.id.item_swipe_left_indicator).setAlpha(scrollProgressPercent > 0 ? scrollProgressPercent : 0);
            }
        });


        // Optionally add an OnItemClickListener
        flingContainer.setOnItemClickListener(new SwipeFlingAdapterView.OnItemClickListener() {
            @Override
            public void onItemClicked(int itemPosition, Object dataObject) {
                makeToast(MainActivity.this, "Clicked!");
            }
        });

    }

    static void makeToast(Context ctx, String s) {
        Toast.makeText(ctx, s, Toast.LENGTH_SHORT).show();
    }

}

class MemberAdapter extends BaseAdapter {

        private final LayoutInflater layoutInflater;
        private final Context context;
        private final ArrayList<Pair<String,String>> list = new ArrayList<>();

        public MemberAdapter(Context context) {
            layoutInflater = LayoutInflater.from(context);
            this.context = context;
        }

        @Override
        public int getCount() {
            return list.size();
        }

        @Override
        public Pair<String,String> getItem(int i) {
            return list.get(i);
        }

        @Override
        public long getItemId(int i) {
            return 0;
        }

        @Override
        public View getView(int i, View view, ViewGroup viewGroup) {

            ViewHolder viewHolder;
            if (view == null) {
                view = layoutInflater.inflate(R.layout.item, viewGroup, false);
                viewHolder = new ViewHolder(view);
                view.setTag(viewHolder);
            } else {
                viewHolder = (ViewHolder) view.getTag();
            }

            Pair<String,String> member = getItem(i);


            viewHolder.name.setText(member.first);

            Glide.with(context)
                    .load(member.second)
                    .centerCrop()
                    .into(viewHolder.avatar);

            return view;
        }

        /**
         * @see List#remove(Object)
         */
        public void remove(int i) {
            try {
                list.remove(i);
            }catch(Exception e){
                Log.d("ERROR","Error");
            }
        }

        /**
         */
        public void addAll(List<Pair<String,String>> members) {
            list.addAll(members);
        }

        /**
         */
        public ArrayList<Pair<String,String>> getAll() {
            return list;
        }

        private class ViewHolder {
            TextView name;
            ImageView avatar;

            ViewHolder(View convertView) {
                name = (TextView) convertView.findViewById(R.id.helloText);
                avatar = (ImageView) convertView.findViewById(R.id.foto);
            }
        }

    }




