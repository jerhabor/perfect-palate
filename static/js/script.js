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
                <label for="method" class="active">Delete Step <a href='javascript:void(0);' class='remove_step'>&times;</a></label>
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
                    <label for="ingredient_name" class="active">Ingredient Name <em>(e.g. Ripe Plantain)</em></label>
                </div>
                <div class="input-field col s5 m3">
                    <input id="ingredient_amount" name="ingredient_amount" minlength="5" maxlength="50" type="text" class="validate" required>
                    <label for="ingredient_amount" class="active">Amount <em>(e.g. 3 tablespoons)</em></label>
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


    // Validation of the 'is_Vegetarian' select (Code inspired by Tim Nelson, Code Institute)
    validateIsVegetarian();
    function validateIsVegetarian() {
        let validInput = { "border-bottom": "1px solid #4caf50", "box-shadow": "0 1px 0 0 #4caf50" };
        let invalidInput = { "border-bottom": "1px solid #f44336", "box-shadow": "0 1px 0 0 #f44336" };
        if ($("select.validate").prop("required")) {
            $("select.validate").css({ "display": "block", "height": "0", "padding": "0", "width": "0", "position": "absolute" });
        }
        $(".select-wrapper input.select-dropdown").on("focusin", function () {
            $(this).parent(".select-wrapper").on("change", function () {
                if ($(this).children("ul").children("li.selected:not(.disabled)").on("click", function () { })) {
                    $(this).children("input").css(validInput);
                }
            });
        }).on("click", function () {
            if ($(this).parent(".select-wrapper").children("ul").children("li.selected:not(.disabled)").css("background-color") === "rgba(0, 0, 0, 0.03)") {
                $(this).parent(".select-wrapper").children("input").css(validInput);
            } else {
                $(".select-wrapper input.select-dropdown").on("focusout", function () {
                    if ($(this).parent(".select-wrapper").children("select").prop("required")) {
                        if ($(this).css("border-bottom") != "1px solid rgb(76, 175, 80)") {
                            $(this).parent(".select-wrapper").children("input").css(invalidInput);
                        }
                    }
                });
            }
        });
    }
});