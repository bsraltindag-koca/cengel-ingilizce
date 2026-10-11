package io.github.bsraltindagkoca.kanca;

import android.graphics.Color;
import android.view.View;
import android.view.Window;

import androidx.core.view.WindowInsetsControllerCompat;

import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * Colours the strips behind the status bar and the navigation bar to match the app theme.
 * On Android 15+ apps are drawn edge to edge and the old "status bar colour" call is ignored,
 * so the window background behind the bars is painted instead, and the bar icons are switched
 * between dark (light theme) and light (dark theme).
 */
@CapacitorPlugin(name = "ThemeBars")
public class ThemeBarsPlugin extends Plugin {

    @PluginMethod
    public void set(PluginCall call) {
        final boolean dark = Boolean.TRUE.equals(call.getBoolean("dark", false));
        final String color = call.getString("color", dark ? "#0e0f1c" : "#f1f2f8");
        getActivity().runOnUiThread(() -> {
            try {
                Window window = getActivity().getWindow();
                View decor = window.getDecorView();
                int c = Color.parseColor(color);
                decor.setBackgroundColor(c);
                window.setStatusBarColor(c);
                window.setNavigationBarColor(c);
                WindowInsetsControllerCompat bars = new WindowInsetsControllerCompat(window, decor);
                bars.setAppearanceLightStatusBars(!dark);
                bars.setAppearanceLightNavigationBars(!dark);
                call.resolve(new JSObject());
            } catch (Exception e) {
                call.reject("Could not style the system bars", e);
            }
        });
    }
}
