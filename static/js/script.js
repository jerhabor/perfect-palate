$(document).ready(function() {
    $('.sidenav').sidenav({ edge: "right" });
    $('.collapsible').collapsible();
    $('.tooltipped').tooltip();
    $('input#input_text, textarea#textarea2').characterCounter();
    $('select').formSelect();

    // This function allows the user to click for more rows as they input their steps to preparing the recipe
    $("#add_step").click(function() {
        $(".method_steps").append(
            `<li>
                <textarea id="method" name="method" type="text" class="validate materialize-textarea" required></textarea>
                <label for="method">Delete Step <a href='javascript:void(0);' class='remove_step'>&times;</a></label>
            </li>`
        );
        $("#first_method").empty();
        $("#first_method").text("Delete Step ") 
        $("#first_method").append(`<a href='javascript:void(0);' class='remove_step'>&times;</a>`)
    });

    $("#add_ingredient").click(function() {
        $(".ingredient_items").append(
            `<li>
                <div class="input-field col s6 m8">
                    <input id="ingredient_name" name="ingredient_name" minlength="5" maxlength="50" type="text" class="validate" required>
                    <label for="ingredient_name">Ingredient Name <em>(e.g. Ripe Plantain)</em></label>
                </div>
                <div class="input-field col s5 m3">
                    <input id="ingredient_amount" name="ingredient_amount" minlength="5" maxlength="50" type="text" class="validate" required>
                    <label for="ingredient_amount">Amount <em>(e.g. 3 tablespoons)</em></label>
                </div>
                <div class="input-field col s1 m1">
                    <button class='remove_ingredient red'><i class="fa fa-times"></i></button>
                </div>
            </li>`
        );
    });

    $(document).on("click", "button.remove_ingredient", function() {
        $(this).parent().parent().remove();
    });

    $(document).on("click", "a.remove_step", function() {
        if ($(".method_steps li").length == 1) {
            $("#first_method").empty();
            $("#first_method").text("What Should I do?");
        } else {   
            $(this).parent().parent().remove();
        };
    });
});