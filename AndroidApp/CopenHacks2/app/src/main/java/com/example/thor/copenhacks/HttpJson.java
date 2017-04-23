package com.example.thor.copenhacks;

import android.os.AsyncTask;
import android.telecom.Call;

import com.google.gson.Gson;
import com.google.gson.internal.ObjectConstructor;
import com.google.gson.reflect.TypeToken;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Created by thor on 23/04/17.
 */

public class HttpJson extends AsyncTask<String, Void, List<ServerResponse>> {
    public interface Callback {
        void onResponse(List<ServerResponse> t);
    }

    private Callback callback;

    public HttpJson setCallback(Callback cb) {
        callback = cb;
        return this;
    }

    @Override
    protected List<ServerResponse> doInBackground(String... params) {
        String url = params[0];
        String json = getJSON(url, 60 * 1000);
        Type listType = new TypeToken<ArrayList<ServerResponse>>(){}.getType();
        List<ServerResponse> res = new Gson().fromJson(json, listType);
        return res;
    }

    public String getJSON(String url, int timeout) {
        HttpURLConnection c = null;
        try {
            URL u = new URL(url);
            c = (HttpURLConnection) u.openConnection();
            c.setRequestMethod("GET");
            c.setRequestProperty("Content-length", "0");
            c.setUseCaches(false);
            c.setAllowUserInteraction(false);
            c.setConnectTimeout(timeout);
            c.setReadTimeout(timeout);
            c.connect();
            int status = c.getResponseCode();

            switch (status) {
                case 200:
                case 201:
                    BufferedReader br = new BufferedReader(new InputStreamReader(c.getInputStream()));
                    StringBuilder sb = new StringBuilder();
                    String line;
                    while ((line = br.readLine()) != null) {
                        sb.append(line + "\n");
                    }
                    br.close();
                    return sb.toString();
            }

        } catch (MalformedURLException ex) {
            Logger.getLogger(getClass().getName()).log(Level.SEVERE, null, ex);
        } catch (IOException ex) {
            Logger.getLogger(getClass().getName()).log(Level.SEVERE, null, ex);
        } finally {
            if (c != null) {
                try {
                    c.disconnect();
                } catch (Exception ex) {
                    Logger.getLogger(getClass().getName()).log(Level.SEVERE, null, ex);
                }
            }
        }
        return null;
    }


    @Override
    protected void onPostExecute(List<ServerResponse> t) {
        super.onPostExecute(t);
        if (t != null&& callback !=null) callback.onResponse(t);
    }
}
