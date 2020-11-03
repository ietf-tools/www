// This whole file comes from https://dequeuniversity.com/library/aria/date-picker with minor tweaks which are:
// - Instead of setting option for a single date picker, they are set as default
// - Addition of the date format
// - Make it work with multiple date pickers. I marked changed lines with at !!change comment, with the original version in comments below it.
// To make it work, both the date picker input and their label must have an id attribute.

$.datepicker.setDefaults({
    dateFormat: 'dd/mm/yy',
    showOn: 'button',
    buttonImageOnly: false,
    buttonText: '',
    dayNamesShort: [
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday',
    ],
    showButtonPanel: true,
    closeText: 'Close',
    onClose: cleanUp,
});

// Add aria-describedby to the button referring to the label
$(function () {
    // !!change
    $('.ui-datepicker-trigger').each(function () {
        $(this).attr('aria-label', 'Calendar view');
        const label = $(`label[for='${$(this).prev('input').attr('id')}']`)[0];
        const labelId = $(label).attr('id');
        if (labelId) {
            $(this).attr('aria-describedby', labelId);
        }
    });
    // $('.ui-datepicker-trigger').attr('aria-describedby', 'datepickerLabel');
    dayTripper();
});

function dayTripper() {
    $('.ui-datepicker-trigger').click(function () {
        var _this = this;
        setTimeout(function () {
            var today = $('.ui-datepicker-today a')[0];

            if (!today) {
                today = $('.ui-state-active')[0] || $('.ui-state-default')[0];
            }

            // Hide the entire page (except the date picker)
            // from screen readers to prevent document navigation
            // (by headings, etc.) while the popup is open
            // !!change
            $('main').addClass('datepicker-hide');
            $('aside').addClass('datepicker-hide');
            $('header').addClass('datepicker-hide');
            $('footer').addClass('datepicker-hide');
            $('nav').addClass('datepicker-hide');
            $('.datepicker-hide').attr('aria-hidden', 'true');
            // $('main').attr('id', 'dp-container');
            // $('#dp-container').attr('aria-hidden', 'true');
            // $('#skipnav').attr('aria-hidden', 'true');

            // Hide the "today" button because it doesn't do what
            // you think it supposed to do
            $('.ui-datepicker-current').hide();

            today.focus();
            //  !!change
            const inputId = $(_this).prev('input').attr('id');
            if (inputId) {
                $('#ui-datepicker-div').attr('data-current-input', inputId);
                datePickHandler(inputId);
            }
            // datePickHandler();
            $(document).on(
                'click',
                '#ui-datepicker-div .ui-datepicker-close',
                function () {
                    closeCalendar();
                },
            );
        }, 0);
    });
}

// !!change
function datePickHandler(inputId) {
    // function datePickHandler() {
    var activeDate;
    var container = document.getElementById('ui-datepicker-div');
    // !!change
    var input = document.getElementById(inputId);
    // var input = document.getElementById('datepicker');

    if (!container || !input) {
        return;
    }

    $(container).find('table').first().attr('role', 'grid');

    container.setAttribute('role', 'application');
    container.setAttribute('aria-label', 'Calendar view date-picker');

    // the top controls:
    var prev = $('.ui-datepicker-prev', container)[0],
        next = $('.ui-datepicker-next', container)[0];

    // This is the line that needs to be fixed for use on pages with base URL set in head
    next.href = 'javascript:void(0)';
    prev.href = 'javascript:void(0)';

    next.setAttribute('role', 'button');
    next.removeAttribute('title');
    prev.setAttribute('role', 'button');
    prev.removeAttribute('title');

    appendOffscreenMonthText(next);
    appendOffscreenMonthText(prev);

    // delegation won't work here for whatever reason, so we are
    // forced to attach individual click listeners to the prev /
    // next month buttons each time they are added to the DOM
    $(next).on('click', handleNextClicks);
    $(prev).on('click', handlePrevClicks);

    monthDayYearText();

    $(container).on('keydown', function calendarKeyboardListener(keyVent) {
        var which = keyVent.which;
        var target = keyVent.target;
        var dateCurrent = getCurrentDate(container);

        if (!dateCurrent) {
            dateCurrent = $('a.ui-state-default')[0];
            setHighlightState(dateCurrent, container);
        }

        if (27 === which) {
            keyVent.stopPropagation();
            return closeCalendar();
        } else if (which === 9 && keyVent.shiftKey) {
            // SHIFT + TAB
            keyVent.preventDefault();
            if ($(target).hasClass('ui-datepicker-close')) {
                // close button
                $('.ui-datepicker-prev')[0].focus();
            } else if ($(target).hasClass('ui-state-default')) {
                // a date link
                $('.ui-datepicker-close')[0].focus();
            } else if ($(target).hasClass('ui-datepicker-prev')) {
                // the prev link
                $('.ui-datepicker-next')[0].focus();
            } else if ($(target).hasClass('ui-datepicker-next')) {
                // the next link
                activeDate =
                    $('.ui-state-highlight') || $('.ui-state-active')[0];
                if (activeDate) {
                    activeDate.focus();
                }
            }
        } else if (which === 9) {
            // TAB
            keyVent.preventDefault();
            if ($(target).hasClass('ui-datepicker-close')) {
                // close button
                activeDate =
                    $('.ui-state-highlight') || $('.ui-state-active')[0];
                if (activeDate) {
                    activeDate.focus();
                }
            } else if ($(target).hasClass('ui-state-default')) {
                $('.ui-datepicker-next')[0].focus();
            } else if ($(target).hasClass('ui-datepicker-next')) {
                $('.ui-datepicker-prev')[0].focus();
            } else if ($(target).hasClass('ui-datepicker-prev')) {
                $('.ui-datepicker-close')[0].focus();
            }
        } else if (which === 37) {
            // LEFT arrow key
            // if we're on a date link...
            if (
                !$(target).hasClass('ui-datepicker-close') &&
                $(target).hasClass('ui-state-default')
            ) {
                keyVent.preventDefault();
                previousDay(target);
            }
        } else if (which === 39) {
            // RIGHT arrow key
            // if we're on a date link...
            if (
                !$(target).hasClass('ui-datepicker-close') &&
                $(target).hasClass('ui-state-default')
            ) {
                keyVent.preventDefault();
                nextDay(target);
            }
        } else if (which === 38) {
            // UP arrow key
            if (
                !$(target).hasClass('ui-datepicker-close') &&
                $(target).hasClass('ui-state-default')
            ) {
                keyVent.preventDefault();
                upHandler(target, container, prev);
            }
        } else if (which === 40) {
            // DOWN arrow key
            if (
                !$(target).hasClass('ui-datepicker-close') &&
                $(target).hasClass('ui-state-default')
            ) {
                keyVent.preventDefault();
                downHandler(target, container, next);
            }
        } else if (which === 13) {
            // ENTER
            if ($(target).hasClass('ui-state-default')) {
                setTimeout(function () {
                    closeCalendar();
                }, 100);
            } else if ($(target).hasClass('ui-datepicker-prev')) {
                handlePrevClicks();
            } else if ($(target).hasClass('ui-datepicker-next')) {
                handleNextClicks();
            }
        } else if (32 === which) {
            if (
                $(target).hasClass('ui-datepicker-prev') ||
                $(target).hasClass('ui-datepicker-next')
            ) {
                target.click();
            }
        } else if (33 === which) {
            // PAGE UP
            moveOneMonth(target, 'prev');
        } else if (34 === which) {
            // PAGE DOWN
            moveOneMonth(target, 'next');
        } else if (36 === which) {
            // HOME
            var firstOfMonth = $(target)
                .closest('tbody')
                .find('.ui-state-default')[0];
            if (firstOfMonth) {
                firstOfMonth.focus();
                setHighlightState(firstOfMonth, $('#ui-datepicker-div')[0]);
            }
        } else if (35 === which) {
            // END
            var $daysOfMonth = $(target)
                .closest('tbody')
                .find('.ui-state-default');
            var lastDay = $daysOfMonth[$daysOfMonth.length - 1];
            if (lastDay) {
                lastDay.focus();
                setHighlightState(lastDay, $('#ui-datepicker-div')[0]);
            }
        }
        $('.ui-datepicker-current').hide();
    });
}

function closeCalendar() {
    var container = $('#ui-datepicker-div');
    $(container).off('keydown');
    // !!change
    var inputId = container.attr('data-current-input');
    var input = $(`#${inputId}`)[0];
    // var input = $('#datepicker')[0];
    $(input).datepicker('hide');

    input.focus();
}

// !!change
function cleanUp() {
    // function removeAria() {
    // make the rest of the page accessible again:
    // !! change
    $('.datepicker-hide').removeAttr('aria-hidden');
    // $("#dp-container").removeAttr('aria-hidden');
    // $("#skipnav").removeAttr('aria-hidden');
}

///////////////////////////////
//////////////////////////// //
///////////////////////// // //
// UTILITY-LIKE THINGS // // //
///////////////////////// // //
//////////////////////////// //
///////////////////////////////
function isOdd(num) {
    return num % 2;
}

function moveOneMonth(currentDate, dir) {
    var button =
        dir === 'next'
            ? $('.ui-datepicker-next')[0]
            : $('.ui-datepicker-prev')[0];

    if (!button) {
        return;
    }

    var ENABLED_SELECTOR =
        '#ui-datepicker-div tbody td:not(.ui-state-disabled)';
    var $currentCells = $(ENABLED_SELECTOR);
    var currentIdx = $.inArray(currentDate.parentNode, $currentCells);

    button.click();
    setTimeout(function () {
        updateHeaderElements();

        var $newCells = $(ENABLED_SELECTOR);
        var newTd = $newCells[currentIdx];
        var newAnchor = newTd && $(newTd).find('a')[0];

        while (!newAnchor) {
            currentIdx--;
            newTd = $newCells[currentIdx];
            newAnchor = newTd && $(newTd).find('a')[0];
        }

        setHighlightState(newAnchor, $('#ui-datepicker-div')[0]);
        newAnchor.focus();
    }, 0);
}

function handleNextClicks() {
    setTimeout(function () {
        updateHeaderElements();
        prepHighlightState();
        $('.ui-datepicker-next').focus();
        $('.ui-datepicker-current').hide();
    }, 0);
}

function handlePrevClicks() {
    setTimeout(function () {
        updateHeaderElements();
        prepHighlightState();
        $('.ui-datepicker-prev').focus();
        $('.ui-datepicker-current').hide();
    }, 0);
}

function previousDay(dateLink) {
    var container = document.getElementById('ui-datepicker-div');
    if (!dateLink) {
        return;
    }
    var td = $(dateLink).closest('td');
    if (!td) {
        return;
    }

    var prevTd = $(td).prev(),
        prevDateLink = $('a.ui-state-default', prevTd)[0];

    if (prevTd && prevDateLink) {
        setHighlightState(prevDateLink, container);
        prevDateLink.focus();
    } else {
        handlePrevious(dateLink);
    }
}

function handlePrevious(target) {
    var container = document.getElementById('ui-datepicker-div');
    if (!target) {
        return;
    }
    var currentRow = $(target).closest('tr');
    if (!currentRow) {
        return;
    }
    var previousRow = $(currentRow).prev();

    if (!previousRow || previousRow.length === 0) {
        // there is not previous row, so we go to previous month...
        previousMonth();
    } else {
        var prevRowDates = $('td a.ui-state-default', previousRow);
        var prevRowDate = prevRowDates[prevRowDates.length - 1];

        if (prevRowDate) {
            setTimeout(function () {
                setHighlightState(prevRowDate, container);
                prevRowDate.focus();
            }, 0);
        }
    }
}

function previousMonth() {
    var prevLink = $('.ui-datepicker-prev')[0];
    var container = document.getElementById('ui-datepicker-div');
    prevLink.click();
    // focus last day of new month
    setTimeout(function () {
        var trs = $('tr', container),
            lastRowTdLinks = $('td a.ui-state-default', trs[trs.length - 1]),
            lastDate = lastRowTdLinks[lastRowTdLinks.length - 1];

        // updating the cached header elements
        updateHeaderElements();

        setHighlightState(lastDate, container);
        lastDate.focus();
    }, 0);
}

///////////////// NEXT /////////////////
/**
 * Handles right arrow key navigation
 * @param  {HTMLElement} dateLink The target of the keyboard event
 */
function nextDay(dateLink) {
    var container = document.getElementById('ui-datepicker-div');
    if (!dateLink) {
        return;
    }
    var td = $(dateLink).closest('td');
    if (!td) {
        return;
    }
    var nextTd = $(td).next(),
        nextDateLink = $('a.ui-state-default', nextTd)[0];

    if (nextTd && nextDateLink) {
        setHighlightState(nextDateLink, container);
        nextDateLink.focus(); // the next day (same row)
    } else {
        handleNext(dateLink);
    }
}

function handleNext(target) {
    var container = document.getElementById('ui-datepicker-div');
    if (!target) {
        return;
    }
    var currentRow = $(target).closest('tr'),
        nextRow = $(currentRow).next();

    if (!nextRow || nextRow.length === 0) {
        nextMonth();
    } else {
        var nextRowFirstDate = $('a.ui-state-default', nextRow)[0];
        if (nextRowFirstDate) {
            setHighlightState(nextRowFirstDate, container);
            nextRowFirstDate.focus();
        }
    }
}

function nextMonth() {
    nextMon = $('.ui-datepicker-next')[0];
    var container = document.getElementById('ui-datepicker-div');
    nextMon.click();
    // focus the first day of the new month
    setTimeout(function () {
        // updating the cached header elements
        updateHeaderElements();

        var firstDate = $('a.ui-state-default', container)[0];
        setHighlightState(firstDate, container);
        firstDate.focus();
    }, 0);
}

/////////// UP ///////////
/**
 * Handle the up arrow navigation through dates
 * @param  {HTMLElement} target   The target of the keyboard event (day)
 * @param  {HTMLElement} cont     The calendar container
 * @param  {HTMLElement} prevLink Link to navigate to previous month
 */
function upHandler(target, cont, prevLink) {
    prevLink = $('.ui-datepicker-prev')[0];
    var rowContext = $(target).closest('tr');
    if (!rowContext) {
        return;
    }
    var rowTds = $('td', rowContext),
        rowLinks = $('a.ui-state-default', rowContext),
        targetIndex = $.inArray(target, rowLinks),
        prevRow = $(rowContext).prev(),
        prevRowTds = $('td', prevRow),
        parallel = prevRowTds[targetIndex],
        linkCheck = $('a.ui-state-default', parallel)[0];

    if (prevRow && parallel && linkCheck) {
        // there is a previous row, a td at the same index
        // of the target AND theres a link in that td
        setHighlightState(linkCheck, cont);
        linkCheck.focus();
    } else {
        // we're either on the first row of a month, or we're on the
        // second and there is not a date link directly above the target
        prevLink.click();
        setTimeout(function () {
            // updating the cached header elements
            updateHeaderElements();
            var newRows = $('tr', cont),
                lastRow = newRows[newRows.length - 1],
                lastRowTds = $('td', lastRow),
                tdParallelIndex = $.inArray(target.parentNode, rowTds),
                newParallel = lastRowTds[tdParallelIndex],
                newCheck = $('a.ui-state-default', newParallel)[0];

            if (lastRow && newParallel && newCheck) {
                setHighlightState(newCheck, cont);
                newCheck.focus();
            } else {
                // theres no date link on the last week (row) of the new month
                // meaning its an empty cell, so we'll try the 2nd to last week
                var secondLastRow = newRows[newRows.length - 2],
                    secondTds = $('td', secondLastRow),
                    targetTd = secondTds[tdParallelIndex],
                    linkCheck = $('a.ui-state-default', targetTd)[0];

                if (linkCheck) {
                    setHighlightState(linkCheck, cont);
                    linkCheck.focus();
                }
            }
        }, 0);
    }
}

//////////////// DOWN ////////////////
/**
 * Handles down arrow navigation through dates in calendar
 * @param  {HTMLElement} target   The target of the keyboard event (day)
 * @param  {HTMLElement} cont     The calendar container
 * @param  {HTMLElement} nextLink Link to navigate to next month
 */
function downHandler(target, cont, nextLink) {
    nextLink = $('.ui-datepicker-next')[0];
    var targetRow = $(target).closest('tr');
    if (!targetRow) {
        return;
    }
    var targetCells = $('td', targetRow),
        cellIndex = $.inArray(target.parentNode, targetCells), // the td (parent of target) index
        nextRow = $(targetRow).next(),
        nextRowCells = $('td', nextRow),
        nextWeekTd = nextRowCells[cellIndex],
        nextWeekCheck = $('a.ui-state-default', nextWeekTd)[0];

    if (nextRow && nextWeekTd && nextWeekCheck) {
        // theres a next row, a TD at the same index of `target`,
        // and theres an anchor within that td
        setHighlightState(nextWeekCheck, cont);
        nextWeekCheck.focus();
    } else {
        nextLink.click();

        setTimeout(function () {
            // updating the cached header elements
            updateHeaderElements();

            var nextMonthTrs = $('tbody tr', cont),
                firstTds = $('td', nextMonthTrs[0]),
                firstParallel = firstTds[cellIndex],
                firstCheck = $('a.ui-state-default', firstParallel)[0];

            if (firstParallel && firstCheck) {
                setHighlightState(firstCheck, cont);
                firstCheck.focus();
            } else {
                // lets try the second row b/c we didnt find a
                // date link in the first row at the target's index
                var secondRow = nextMonthTrs[1],
                    secondTds = $('td', secondRow),
                    secondRowTd = secondTds[cellIndex],
                    secondCheck = $('a.ui-state-default', secondRowTd)[0];

                if (secondRow && secondCheck) {
                    setHighlightState(secondCheck, cont);
                    secondCheck.focus();
                }
            }
        }, 0);
    }
}

function onCalendarHide() {
    closeCalendar();
}

// add an aria-label to the date link indicating the currently focused date
// (formatted identically to the required format: mm/dd/yyyy)
function monthDayYearText() {
    var cleanUps = $('.amaze-date');

    $(cleanUps).each(function (clean) {
        // each(cleanUps, function (clean) {
        clean.parentNode.removeChild(clean);
    });

    var datePickDiv = document.getElementById('ui-datepicker-div');
    // in case we find no datepick div
    if (!datePickDiv) {
        return;
    }

    var dates = $('a.ui-state-default', datePickDiv);
    $(dates)
        .attr('role', 'button')
        .on('keydown', function (e) {
            if (e.which === 32) {
                e.preventDefault();
                e.target.click();
                setTimeout(function () {
                    closeCalendar();
                }, 100);
            }
        });
    $(dates).each(function (index, date) {
        var currentRow = $(date).closest('tr'),
            currentTds = $('td', currentRow),
            currentIndex = $.inArray(date.parentNode, currentTds),
            headThs = $('thead tr th', datePickDiv),
            dayIndex = headThs[currentIndex],
            daySpan = $('span', dayIndex)[0],
            monthName = $('.ui-datepicker-month', datePickDiv)[0].innerHTML,
            year = $('.ui-datepicker-year', datePickDiv)[0].innerHTML,
            number = date.innerHTML;

        if (!daySpan || !monthName || !number || !year) {
            return;
        }

        // AT Reads: {month} {date} {year} {day}
        // "December 18 2014 Thursday"
        var dateText =
            date.innerHTML + ' ' + monthName + ' ' + year + ' ' + daySpan.title;
        // AT Reads: {date(number)} {name of day} {name of month} {year(number)}
        // var dateText = date.innerHTML + ' ' + daySpan.title + ' ' + monthName + ' ' + year;
        // add an aria-label to the date link reading out the currently focused date
        date.setAttribute('aria-label', dateText);
    });
}

// update the cached header elements because we're in a new month or year
function updateHeaderElements() {
    var context = document.getElementById('ui-datepicker-div');
    if (!context) {
        return;
    }

    //  $(context).find('table').first().attr('role', 'grid');

    prev = $('.ui-datepicker-prev', context)[0];
    next = $('.ui-datepicker-next', context)[0];

    //make them click/focus - able
    next.href = 'javascript:void(0)';
    prev.href = 'javascript:void(0)';

    next.setAttribute('role', 'button');
    prev.setAttribute('role', 'button');
    appendOffscreenMonthText(next);
    appendOffscreenMonthText(prev);

    $(next).on('click', handleNextClicks);
    $(prev).on('click', handlePrevClicks);

    // add month day year text
    monthDayYearText();
}

function prepHighlightState() {
    var highlight;
    var cage = document.getElementById('ui-datepicker-div');
    highlight =
        $('.ui-state-highlight', cage)[0] || $('.ui-state-default', cage)[0];
    if (highlight && cage) {
        setHighlightState(highlight, cage);
    }
}

// Set the highlighted class to date elements, when focus is received
function setHighlightState(newHighlight, container) {
    var prevHighlight = getCurrentDate(container);
    // remove the highlight state from previously
    // highlighted date and add it to our newly active date
    $(prevHighlight).removeClass('ui-state-highlight');
    $(newHighlight).addClass('ui-state-highlight');
}

// grabs the current date based on the highlight class
function getCurrentDate(container) {
    var currentDate = $('.ui-state-highlight', container)[0];
    return currentDate;
}

/**
 * Appends logical next/prev month text to the buttons
 * - ex: Next Month, January 2015
 *       Previous Month, November 2014
 */
function appendOffscreenMonthText(button) {
    var buttonText;
    var isNext = $(button).hasClass('ui-datepicker-next');
    var months = [
        'january',
        'february',
        'march',
        'april',
        'may',
        'june',
        'july',
        'august',
        'september',
        'october',
        'november',
        'december',
    ];

    var currentMonth = $('.ui-datepicker-title .ui-datepicker-month')
        .text()
        .toLowerCase();
    var monthIndex = $.inArray(currentMonth.toLowerCase(), months);
    var currentYear = $('.ui-datepicker-title .ui-datepicker-year')
        .text()
        .toLowerCase();
    var adjacentIndex = isNext ? monthIndex + 1 : monthIndex - 1;

    if (isNext && currentMonth === 'december') {
        currentYear = parseInt(currentYear, 10) + 1;
        adjacentIndex = 0;
    } else if (!isNext && currentMonth === 'january') {
        currentYear = parseInt(currentYear, 10) - 1;
        adjacentIndex = months.length - 1;
    }

    buttonText = isNext
        ? 'Next<span class="sr-only"> Month, ' +
          firstToCap(months[adjacentIndex]) +
          ' ' +
          currentYear
        : '<span aria-hidden="true">Prev</span><span class="sr-only">Previous Month, ' +
          firstToCap(months[adjacentIndex]) +
          ' ' +
          currentYear +
          '</span>';

    $(button).find('.ui-icon').html(buttonText);
}

// Returns the string with the first letter capitalized
function firstToCap(s) {
    return s.charAt(0).toUpperCase() + s.slice(1);
}
