$(document).ready(function() {

    // Initiation for side navigation bar on mobile when
    // user clicks the 'hamburger' icon
    $('.sidenav').sidenav({ edge: "right" });

    // Initiation for tooltip which gives user a first-hand
    // indication of whether a recipe is suitable for vegeterians
    $('.tooltipped').tooltip();

    // Initiation for textarea element used in 'description'
    // and 'steps' as user adds a new recipe
    $('input#input_text, textarea#textarea2').characterCounter();

    // Initiation for the 'is_vegetarian' select/dropdown when
    // user adds a new recipe
    $('select').formSelect();

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

    // This function allows the user to click for more rows 
    // as they input their steps to preparing the recipe
    $("#add_step").click(function() {
        $(".method-steps").append(
        `<div class="input-field col s11">
            <textarea id="method" name="method" type="text" 
                class="validate materialize-textarea"></textarea>
        </div>`
        );
    });

    // This function allows the user to click for more rows 
    // as they add required ingredients for the recipe
    $("#add_ingredient").click(function() {
        $(".ingredient_items").append(
            `<li>
                <div class="input-field col s6 m8">
                    <input id="ingredient_name" name="ingredient_name" minlength="5" maxlength="50" type="text" class="validate">
                    <label for="ingredient_name" class="active">Ingredient Name <em>(e.g. Ripe Plantain)</em></label>
                </div>
                <div class="input-field col s5 m3">
                    <input id="ingredient_amount" name="ingredient_amount" minlength="5" maxlength="50" type="text" class="validate">
                    <label for="ingredient_amount" class="active">Amount <em>(e.g. 3 tablespoons)</em></label>
                </div>
                <div class="input-field col s1 m1">
                    <button class="remove_ingredient red"><i class="fa fa-times"></i></button>
                </div>
            </li>`
        );
    });

    // This function allows the user to delete rows when editing 
    // their steps/ingredients to preparing the recipe
    $(document).on("click", function() {
        $(this).parent().parent().remove();
    });
});